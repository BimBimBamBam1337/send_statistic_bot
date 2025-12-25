from .user import router as user_router
from .channel import router as channel_router
from .excel_tabel import router as excel_tabel_router


routers = [user_router, channel_router, excel_tabel_router]
