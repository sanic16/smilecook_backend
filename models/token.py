from extensions import db

class TokenBlocklist(db.Model):
    __tablename__ = 'token_blocklist'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    token_type = db.Column(db.String(10), nullable=False)
    user_identity = db.Column(db.String(50), nullable=False)
    revoked = db.Column(db.Boolean(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())

    def save(self):
        db.session.add(self)
        db.session.commit()    
