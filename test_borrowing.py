"""
Test Borrowing Workflow
=======================
Demonstrates the complete physical book borrowing and return flow.
"""

from app import create_app, db
from app.models.physical_book import PhysicalBook
from app.models.user import User
from app.models.loan import Loan
from app.models.fine import Fine
from app.models import LoanStatusEnum
from datetime import datetime, timedelta

def test_complete_workflow():
    """Test the complete borrowing workflow with fine calculation."""
    
    print("\n" + "="*70)
    print("🔄 TESTING PHYSICAL BOOK BORROWING WORKFLOW")
    print("="*70)
    
    # Step 1: Find a book
    book = PhysicalBook.query.filter(
        PhysicalBook.available_copies > 0
    ).first()
    
    if not book:
        print("\n❌ No books available for testing.")
        print("💡 Run 'python seed_physical_books.py' first.\n")
        return
        
        print(f"\n✅ Step 1: Book Selected")
        print(f"   Title: {book.title}")
        print(f"   Available: {book.available_copies}/{book.total_copies}")
        
        # Step 2: Find or create a test student
        student = User.query.first()
        
        if not student:
            print("\n❌ No students in database.")
            print("💡 Register a student first through the app.\n")
            return
        
        print(f"\n✅ Step 2: Student Ready")
        print(f"   Name: {student.name}")
        print(f"   Email: {student.email}")
        
        # Step 3: Create loan (simulating borrowing)
        print(f"\n📤 Step 3: Creating Loan...")
        
        initial_available = book.available_copies
        
        loan = Loan(
            student_id=student.id,
            book_id=book.id,
            borrowed_date=datetime.utcnow(),
            due_date=datetime.utcnow() + timedelta(days=14),  # 2 weeks
            status=LoanStatusEnum.BORROWED
        )
        
        # Reduce available copies
        book.available_copies -= 1
        
        db.session.add(loan)
        db.session.commit()
        
        print(f"   ✅ Loan created successfully!")
        print(f"   Loan ID: {loan.id}")
        print(f"   Borrowed: {loan.borrowed_date.strftime('%Y-%m-%d %H:%M')}")
        print(f"   Due: {loan.due_date.strftime('%Y-%m-%d %H:%M')}")
        print(f"   Available copies: {initial_available} → {book.available_copies}")
        
        # Step 4: Simulate overdue return
        print(f"\n⏰ Step 4: Simulating Overdue Return...")
        
        # Make it overdue by setting due date in past
        loan.due_date = datetime.utcnow() - timedelta(days=5)
        loan.returned_date = datetime.utcnow()
        loan.status = LoanStatusEnum.RETURNED
        
        # Increase available copies
        book.available_copies += 1
        
        # Create fine (₹200 as per your requirement)
        fine = Fine.create_standard_fine(loan_id=loan.id)
        
        db.session.add(fine)
        db.session.commit()
        
        print(f"   ✅ Book returned (5 days late)")
        print(f"   Available copies: {book.available_copies - 1} → {book.available_copies}")
        print(f"   Fine Created: ₹{fine.amount}")
        print(f"   Fine Status: {fine.status.value}")
        
        # Step 5: Show fine details
        print(f"\n💰 Step 5: Fine Details")
        print(f"   Fine ID: {fine.id}")
        print(f"   Amount: ₹{fine.amount}")
        print(f"   Paid: ₹{fine.paid_amount}")
        print(f"   Balance: ₹{fine.balance}")
        print(f"   Status: {fine.status.value.upper()}")
        
        # Step 6: Simulate payment
        print(f"\n💳 Step 6: Processing Payment...")
        
        from app.models import FineStatusEnum
        fine.paid_amount = fine.amount
        fine.status = FineStatusEnum.PAID
        
        db.session.commit()
        
        print(f"   ✅ Payment successful!")
        print(f"   Paid: ₹{fine.paid_amount}")
        print(f"   Balance: ₹{fine.balance}")
        print(f"   Status: {fine.status.value.upper()}")
        
        # Cleanup for next test
        print(f"\n🧹 Cleaning up test data...")
        db.session.delete(fine)
        db.session.delete(loan)
        db.session.commit()
        print(f"   ✅ Test data removed")
        
        print("\n" + "="*70)
        print("✅ WORKFLOW TEST COMPLETE")
        print("="*70)
        print("\n💡 Summary:")
        print("   1. Book borrowed → Available copies decreased")
        print("   2. Book returned late → Fine of ₹200 created")
        print("   3. Fine paid → Status updated to PAID")
        print("   4. Available copies restored")
        print("\n" + "="*70 + "\n")


def show_loan_statistics():
    """Show statistics about loans and fines."""
    
    from app.models import FineStatusEnum
    
    total_loans = Loan.query.count()
    active_loans = Loan.query.filter_by(status=LoanStatusEnum.BORROWED).count()
    returned_loans = Loan.query.filter_by(status=LoanStatusEnum.RETURNED).count()
    overdue_loans = Loan.query.filter(
        Loan.status == LoanStatusEnum.BORROWED,
        Loan.due_date < datetime.utcnow()
    ).count()
    
    total_fines = Fine.query.count()
    pending_fines = Fine.query.filter_by(status=FineStatusEnum.PENDING).count()
    paid_fines = Fine.query.filter_by(status=FineStatusEnum.PAID).count()
    
    total_fine_amount = db.session.query(
        db.func.sum(Fine.amount)
    ).scalar() or 0
    
    total_paid = db.session.query(
        db.func.sum(Fine.paid_amount)
    ).scalar() or 0
    
    total_pending = total_fine_amount - total_paid
    
    print("\n" + "="*70)
    print("📊 LOAN & FINE STATISTICS")
    print("="*70)
    print("\n📚 Loans:")
    print(f"   Total: {total_loans}")
    print(f"   Active: {active_loans}")
    print(f"   Returned: {returned_loans}")
    print(f"   Overdue: {overdue_loans}")
    
    print("\n💰 Fines:")
    print(f"   Total Fines: {total_fines}")
    print(f"   Pending: {pending_fines}")
    print(f"   Paid: {paid_fines}")
    print(f"   Total Amount: ₹{total_fine_amount}")
    print(f"   Collected: ₹{total_paid}")
    print(f"   Pending Amount: ₹{total_pending}")
    print("="*70 + "\n")


if __name__ == '__main__':
    import sys
    
    # Create Flask app instance
    app = create_app()
    
    with app.app_context():
        if len(sys.argv) > 1 and sys.argv[1] == 'stats':
            show_loan_statistics()
        else:
            test_complete_workflow()
