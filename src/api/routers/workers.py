"""
Worker endpoints - Complete CRUD operations for workers.
"""
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from src.db.database import get_db
from src.db.models import Worker

router = APIRouter()


# Pydantic models for request/response
class WorkerBase(BaseModel):
    """Base worker model with common fields."""
    FIRST_NAME: str = Field(..., min_length=1, max_length=255, description="Worker's first name")
    LAST_NAME: str = Field(..., min_length=1, max_length=255, description="Worker's last name")
    SALARY: int = Field(..., gt=0, description="Worker's salary (must be positive)")
    JOINING_DATE: datetime = Field(..., description="Date when worker joined")
    DEPARTMENT: str = Field(..., min_length=1, max_length=255, description="Worker's department")


class WorkerCreate(WorkerBase):
    """Model for creating a new worker."""
    pass


class WorkerUpdate(BaseModel):
    """Model for updating an existing worker (all fields optional)."""
    FIRST_NAME: Optional[str] = Field(None, min_length=1, max_length=255)
    LAST_NAME: Optional[str] = Field(None, min_length=1, max_length=255)
    SALARY: Optional[int] = Field(None, gt=0)
    JOINING_DATE: Optional[datetime] = None
    DEPARTMENT: Optional[str] = Field(None, min_length=1, max_length=255)


class WorkerResponse(WorkerBase):
    """Worker response model."""
    WORKER_ID: int
    
    class Config:
        from_attributes = True  # For Pydantic v2


# CRUD Endpoints

@router.get("/workers", response_model=List[WorkerResponse])
async def get_workers(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    department: Optional[str] = Query(None, description="Filter by department name"),
    db: Session = Depends(get_db)
) -> List[WorkerResponse]:
    """
    Get all workers from the database with optional filtering and pagination.
    
    Args:
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return (1-1000)
        department: Filter by department name (optional)
        db: Database session
        
    Returns:
        List of workers matching the criteria
    """
    query = db.query(Worker)
    
    # Apply department filter if provided
    if department:
        query = query.filter(Worker.DEPARTMENT == department)
    
    # Apply ordering (required by SQL Server for OFFSET/LIMIT)
    query = query.order_by(Worker.WORKER_ID)
    
    # Apply pagination
    workers = query.offset(skip).limit(limit).all()
    return workers


@router.get("/workers/{worker_id}", response_model=WorkerResponse)
async def get_worker(worker_id: int, db: Session = Depends(get_db)) -> WorkerResponse:
    """
    Get a single worker by ID.
    
    Args:
        worker_id: The ID of the worker to retrieve
        db: Database session
        
    Returns:
        Worker details
        
    Raises:
        HTTPException: 404 if worker not found
    """
    worker = db.query(Worker).filter(Worker.WORKER_ID == worker_id).first()
    if not worker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Worker with ID {worker_id} not found"
        )
    return worker


@router.post("/workers", response_model=WorkerResponse, status_code=status.HTTP_201_CREATED)
async def create_worker(worker: WorkerCreate, db: Session = Depends(get_db)) -> WorkerResponse:
    """
    Create a new worker.
    
    Args:
        worker: Worker data to create
        db: Database session
        
    Returns:
        The created worker with assigned ID
    """
    # Create new Worker instance
    db_worker = Worker(
        FIRST_NAME=worker.FIRST_NAME,
        LAST_NAME=worker.LAST_NAME,
        SALARY=worker.SALARY,
        JOINING_DATE=worker.JOINING_DATE,
        DEPARTMENT=worker.DEPARTMENT
    )
    
    # Add to database
    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)  # Get the assigned ID
    
    return db_worker


@router.put("/workers/{worker_id}", response_model=WorkerResponse)
async def update_worker(
    worker_id: int, 
    worker: WorkerUpdate, 
    db: Session = Depends(get_db)
) -> WorkerResponse:
    """
    Update an existing worker.
    
    Args:
        worker_id: The ID of the worker to update
        worker: Updated worker data (only provided fields will be updated)
        db: Database session
        
    Returns:
        The updated worker
        
    Raises:
        HTTPException: 404 if worker not found
    """
    # Find the worker
    db_worker = db.query(Worker).filter(Worker.WORKER_ID == worker_id).first()
    if not db_worker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Worker with ID {worker_id} not found"
        )
    
    # Update only the provided fields
    update_data = worker.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_worker, field, value)
    
    # Save changes
    db.commit()
    db.refresh(db_worker)
    
    return db_worker


@router.delete("/workers/{worker_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_worker(worker_id: int, db: Session = Depends(get_db)) -> None:
    """
    Delete a worker by ID.
    
    Args:
        worker_id: The ID of the worker to delete
        db: Database session
        
    Raises:
        HTTPException: 404 if worker not found
    """
    # Find the worker
    db_worker = db.query(Worker).filter(Worker.WORKER_ID == worker_id).first()
    if not db_worker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Worker with ID {worker_id} not found"
        )
    
    # Delete the worker
    db.delete(db_worker)
    db.commit()


# Additional utility endpoints

@router.get("/workers/departments/list", response_model=List[str])
async def get_departments(db: Session = Depends(get_db)) -> List[str]:
    """
    Get a list of all unique departments.
    
    Returns:
        List of department names
    """
    departments = db.query(Worker.DEPARTMENT).distinct().all()
    return [dept[0] for dept in departments if dept[0]]


@router.get("/workers/stats/summary")
async def get_worker_stats(db: Session = Depends(get_db)):
    """
    Get summary statistics about workers.
    
    Returns:
        Dictionary with worker statistics
    """
    from sqlalchemy import func
    
    # Get basic stats
    total_workers = db.query(Worker).count()
    avg_salary = db.query(func.avg(Worker.SALARY)).scalar() or 0
    min_salary = db.query(func.min(Worker.SALARY)).scalar() or 0
    max_salary = db.query(func.max(Worker.SALARY)).scalar() or 0
    
    # Get department counts
    dept_counts = db.query(
        Worker.DEPARTMENT,
        func.count(Worker.WORKER_ID).label('count')
    ).group_by(Worker.DEPARTMENT).all()
    
    return {
        "total_workers": total_workers,
        "salary_stats": {
            "average": round(float(avg_salary), 2),
            "minimum": min_salary,
            "maximum": max_salary
        },
        "departments": {dept: count for dept, count in dept_counts}
    }