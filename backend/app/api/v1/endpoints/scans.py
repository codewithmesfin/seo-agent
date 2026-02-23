from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.audit import Scan, Page
from app.models.user import User
from app.worker.tasks import scan_domain_task
from app.api.v1.endpoints.auth import get_current_user
from pydantic import BaseModel
from fastapi.responses import Response
from app.services.reports import report_service

router = APIRouter()

class ScanCreate(BaseModel):
    url: str

@router.post("/", response_model=Any)
async def create_scan(
    scan_in: ScanCreate,
    current_user: User = Depends(get_current_user)
) -> Any:
    # Check usage limits (Simple SaaS logic)
    user_scans_count = await Scan.find(Scan.user_id == str(current_user.id)).count()
    if current_user.role == "user" and user_scans_count >= 5:
        raise HTTPException(status_code=403, detail="Free tier limit reached. Upgrade to Pro.")

    scan = Scan(
        user_id=str(current_user.id),
        domain=scan_in.url,
        status="pending"
    )
    await scan.insert()

    # Trigger background task
    scan_domain_task.delay(str(scan.id), scan_in.url)

    return scan

@router.get("/", response_model=List[Any])
async def list_scans(
    current_user: User = Depends(get_current_user)
) -> Any:
    scans = await Scan.find(Scan.user_id == str(current_user.id)).sort("-created_at").to_list()
    return scans

@router.get("/{scan_id}", response_model=Any)
async def get_scan(
    scan_id: str,
    current_user: User = Depends(get_current_user)
) -> Any:
    scan = await Scan.get(scan_id)
    if not scan or scan.user_id != str(current_user.id):
        raise HTTPException(status_code=404, detail="Scan not found")

    pages = await Page.find(Page.scan_id == scan_id).to_list()
    return {
        "scan": scan,
        "pages": pages
    }

@router.get("/{scan_id}/pdf")
async def get_scan_pdf(
    scan_id: str,
    current_user: User = Depends(get_current_user)
) -> Any:
    scan = await Scan.get(scan_id)
    if not scan or scan.user_id != str(current_user.id):
        raise HTTPException(status_code=404, detail="Scan not found")

    pages = await Page.find(Page.scan_id == scan_id).to_list()
    pdf_content = report_service.generate_scan_pdf(scan, pages)

    return Response(
        content=pdf_content,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=report_{scan_id}.pdf"}
    )
