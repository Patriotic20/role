from sqlalchemy.ext.asyncio import AsyncSession

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        
        
    async def create_role(self):
        pass
    
    async def get_role(self):
        pass
    
    async def list_role(self):
        pass
    
    async def update_role(self):
        pass
    
    async def delete_role(self):
        pass
    