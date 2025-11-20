from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.types import JSON
from . import db

class MetadataLedger(db.Model):
    __tablename__ = 'metadata_ledger'
    
    id = Column(Integer, primary_key=True)
    resource_id = Column(Text, nullable=False, index=True)
    metadata = Column(JSON, nullable=False)
    created_by = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    prev_hash = Column(Text, nullable=True)
    entry_hash = Column(Text, nullable=False, unique=True, index=True)
    signature = Column(Text, nullable=True)
    anchor_tx = Column(Text, nullable=True)
    
    def as_dict(self):
        return {
            'id': self.id,
            'resource_id': self.resource_id,
            'metadata': self.metadata,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'prev_hash': self.prev_hash,
            'entry_hash': self.entry_hash,
            'signature': self.signature,
            'anchor_tx': self.anchor_tx,
        }
