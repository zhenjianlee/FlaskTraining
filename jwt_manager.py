import logging

from models import BlockedTokenModel

from flask import jsonify
from flask_jwt_extended import JWTManager

jwt=JWTManager()

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header,jwt_payload):
    logging.debug(f"ℹ️ token_in_blocklist_loader : checking")
    curr_jti=jwt_payload.get('jti')
    blocked_jti = BlockedTokenModel.query.filter_by(jti=curr_jti).first()
    if blocked_jti:
        logging.debug(f"token_in_blocklist_loader : Found blocked JTI : {blocked_jti}. Return TRUE")
        return True
    logging.debug(f"token_in_blocklist_loader : No  JTI  for: {blocked_jti}. Return FALSE")
    return False
    
@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (jsonify({"description":"The token has been revoked","error":"token_revoked"}),401)

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity ==8 :
        return {'isAdmin':True}
    else:
        return {'isAdmin':False}
        
@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header,jwt_payload):
    return(jsonify({
        "message":"The token is not fresh",
        "error":"fresh_token_required"
    }))
        
@jwt.expired_token_loader
def token_expired(jwt_header,jwt_payload):
    return (jsonify({"message":"Token has expired", "error":"token_expired"}),401)
    
@jwt.invalid_token_loader
def invalid_token(error):
    return(jsonify({"message":"Token is invalid","error":error}),401)

@jwt.unauthorized_loader
def unauthorized_token(error):
    return (jsonify({"message":"Token is not authorized","error":error}))