from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from expenses.models import Expense
from .services import OCRService


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_receipt(request, expense_id):
    """Upload receipt and process with OCR"""
    expense = get_object_or_404(Expense, id=expense_id)
    
    # Check if user has permission to modify this expense
    if expense.payer != request.user and not expense.group.members.filter(user=request.user).exists():
        return Response(
            {'error': 'You do not have permission to modify this expense'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    if 'receipt' not in request.FILES:
        return Response(
            {'error': 'No receipt file provided'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    receipt_file = request.FILES['receipt']
    
    # Save the file
    expense.receipt_file = receipt_file
    expense.save()
    
    # Process with OCR
    try:
        ocr_data = OCRService.process_receipt(expense.receipt_file.path)
        
        # Update expense with extracted data
        if ocr_data.get('vendor'):
            expense.vendor = ocr_data['vendor']
        if ocr_data.get('invoice_no'):
            expense.invoice_no = ocr_data['invoice_no']
        if ocr_data.get('date'):
            expense.date = ocr_data['date']
        if ocr_data.get('amount'):
            expense.amount_subtotal = ocr_data['amount']
        if ocr_data.get('gstin'):
            expense.gstin = ocr_data['gstin']
        
        # Store raw OCR data
        expense.ocr_data = ocr_data
        expense.save()
        
        return Response({
            'message': 'Receipt processed successfully',
            'extracted_data': ocr_data,
            'expense': {
                'id': expense.id,
                'vendor': expense.vendor,
                'amount': str(expense.total_amount),
                'invoice_no': expense.invoice_no,
                'date': expense.date,
                'gstin': expense.gstin,
            }
        })
    
    except Exception as e:
        return Response(
            {'error': f'Error processing receipt: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )