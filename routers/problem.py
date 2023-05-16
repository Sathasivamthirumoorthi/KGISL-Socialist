from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from schema import ProblemCreate, ProblemUpdate, ProblemSchema,ProblemWithUserSchema
from model import User, Problem
from security import get_password_hash, authenticate_user, create_access_token, get_current_user,get_db

router = APIRouter(
    tags = ["Problems"]
)



# Create a problem
@router.post("/users/{user_id}/problems", status_code=status.HTTP_201_CREATED)
def create_problem(user_id: int, problem: ProblemCreate, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Create the problem
    db_problem = Problem(**problem.dict(), user_id=user_id)
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    
    return db_problem

# Get a problem by ID
@router.get("/users/{user_id}/problems/{problem_id}", response_model=ProblemSchema)
def get_problem(user_id: int, problem_id: int, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Get the problem
    problem = db.query(Problem).filter(Problem.id == problem_id, Problem.user_id == user_id).first()
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found",
        )
    
    return problem

# Get all problems for a user
@router.get("/users/{user_id}/problems", response_model=List[ProblemSchema])
def get_user_problems(user_id: int, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Get all problems for the user
    problems = db.query(Problem).filter(Problem.user_id == user_id).all()
    return problems

# Update a problem
@router.put("/users/{user_id}/problems/{problem_id}", response_model=ProblemSchema)
def update_problem(user_id: int, problem_id: int, problem: ProblemUpdate, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Get the problem
    db_problem = db.query(Problem).filter(Problem.id == problem_id, Problem.user_id == user_id).first()
    if not db_problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found",
        )
    
    # Update the problem attributes
    for attr, value in problem.dict().items():
        setattr(db_problem, attr, value)
    
    db.commit()
    db.refresh(db_problem)
    
    return db_problem


# Get all problems with user details
@router.get("/problems", response_model=List[ProblemWithUserSchema])
def get_all_problems(db: Session = Depends(get_db)):
    problems = db.query(Problem).join(User).all()
    return problems



@router.delete("/users/{user_id}/problems/{problem_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_problem(user_id: int, problem_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Get the problem
    problem = db.query(Problem).filter(Problem.id == problem_id, Problem.user_id == user_id).first()
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found",
        )

    # Delete the problem
    db.delete(problem)
    db.commit()

    return None