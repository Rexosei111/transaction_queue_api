import hashlib


async def encrypt_otp_with_md5(otp: str):
    return hashlib.md5(otp.encode()).hexdigest()
