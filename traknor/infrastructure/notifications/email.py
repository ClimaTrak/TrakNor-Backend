from django.core.mail import send_mail
from traknor.infrastructure.work_orders.models import WorkOrder


def send_work_order_completed(work_order: WorkOrder) -> None:
    """Send notification that a work order was completed."""
    send_mail(
        subject="Ordem de Serviço Concluída",
        message=f"A Ordem de Serviço {work_order.code} foi concluída.",
        from_email="noreply@example.com",
        recipient_list=[work_order.created_by.email],
    )
