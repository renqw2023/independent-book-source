"""
加密解密工具 - Crypto Utils

提供各种加密解密功能：
- Base64编解码
- MD5哈希
- URL编解码
- 简单加密解密
"""

import base64
import hashlib
import hmac
import json
import logging
import secrets
from typing import Dict, List, Optional, Any, Union
from urllib.parse import quote, unquote


class Crypto:
    """加密解密工具类"""
    
    def __init__(self):
        self.logger = logging.getLogger("crypto")
    
    @staticmethod
    def base64_encode(data: Union[str, bytes]) -> str:
        """Base64编码"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        return base64.b64encode(data).decode('utf-8')
    
    @staticmethod
    def base64_decode(data: str) -> str:
        """Base64解码"""
        try:
            decoded_bytes = base64.b64decode(data)
            return decoded_bytes.decode('utf-8')
        except Exception as e:
            logging.getLogger("crypto").error(f"Base64解码失败: {e}")
            return ""
    
    @staticmethod
    def url_encode(data: str) -> str:
        """URL编码"""
        return quote(data, safe='')
    
    @staticmethod
    def url_decode(data: str) -> str:
        """URL解码"""
        return unquote(data)
    
    @staticmethod
    def md5_hash(data: Union[str, bytes]) -> str:
        """MD5哈希"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        return hashlib.md5(data).hexdigest()
    
    @staticmethod
    def sha1_hash(data: Union[str, bytes]) -> str:
        """SHA1哈希"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        return hashlib.sha1(data).hexdigest()
    
    @staticmethod
    def sha256_hash(data: Union[str, bytes]) -> str:
        """SHA256哈希"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        return hashlib.sha256(data).hexdigest()
    
    @staticmethod
    def hmac_sha256(data: Union[str, bytes], key: Union[str, bytes]) -> str:
        """HMAC-SHA256"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        if isinstance(key, str):
            key = key.encode('utf-8')
        
        return hmac.new(key, data, hashlib.sha256).hexdigest()
    
    @staticmethod
    def generate_random_string(length: int = 16) -> str:
        """生成随机字符串"""
        return secrets.token_hex(length // 2)
    
    @staticmethod
    def simple_encrypt(data: str, key: str) -> str:
        """简单加密（XOR）"""
        if not data or not key:
            return data
        
        key_bytes = key.encode('utf-8')
        data_bytes = data.encode('utf-8')
        
        encrypted = bytearray()
        for i, byte in enumerate(data_bytes):
            encrypted.append(byte ^ key_bytes[i % len(key_bytes)])
        
        return base64.b64encode(encrypted).decode('utf-8')
    
    @staticmethod
    def simple_decrypt(encrypted_data: str, key: str) -> str:
        """简单解密（XOR）"""
        if not encrypted_data or not key:
            return encrypted_data
        
        try:
            key_bytes = key.encode('utf-8')
            encrypted_bytes = base64.b64decode(encrypted_data)
            
            decrypted = bytearray()
            for i, byte in enumerate(encrypted_bytes):
                decrypted.append(byte ^ key_bytes[i % len(key_bytes)])
            
            return decrypted.decode('utf-8')
        except Exception as e:
            logging.getLogger("crypto").error(f"解密失败: {e}")
            return encrypted_data
    
    @staticmethod
    def hex_encode(data: Union[str, bytes]) -> str:
        """十六进制编码"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        return data.hex()
    
    @staticmethod
    def hex_decode(hex_data: str) -> str:
        """十六进制解码"""
        try:
            decoded_bytes = bytes.fromhex(hex_data)
            return decoded_bytes.decode('utf-8')
        except Exception as e:
            logging.getLogger("crypto").error(f"十六进制解码失败: {e}")
            return ""
    
    @staticmethod
    def caesar_cipher(text: str, shift: int = 3) -> str:
        """凯撒密码加密"""
        result = ""
        for char in text:
            if char.isalpha():
                ascii_offset = 65 if char.isupper() else 97
                shifted = (ord(char) - ascii_offset + shift) % 26
                result += chr(shifted + ascii_offset)
            else:
                result += char
        return result
    
    @staticmethod
    def caesar_decipher(text: str, shift: int = 3) -> str:
        """凯撒密码解密"""
        return Crypto.caesar_cipher(text, -shift)
    
    @staticmethod
    def rot13(text: str) -> str:
        """ROT13编码/解码"""
        return Crypto.caesar_cipher(text, 13)
    
    @staticmethod
    def generate_signature(data: Dict[str, Any], secret_key: str) -> str:
        """生成签名"""
        # 按键名排序
        sorted_items = sorted(data.items())
        
        # 构建签名字符串
        sign_string = "&".join([f"{k}={v}" for k, v in sorted_items])
        sign_string += f"&key={secret_key}"
        
        # 生成MD5签名
        return Crypto.md5_hash(sign_string).upper()
    
    @staticmethod
    def verify_signature(data: Dict[str, Any], signature: str, secret_key: str) -> bool:
        """验证签名"""
        expected_signature = Crypto.generate_signature(data, secret_key)
        return signature.upper() == expected_signature
    
    @staticmethod
    def obfuscate_string(text: str) -> str:
        """字符串混淆"""
        if not text:
            return text
        
        # 简单的字符替换混淆
        obfuscated = ""
        for char in text:
            if char.isalnum():
                # 字符偏移
                if char.isdigit():
                    obfuscated += str((int(char) + 5) % 10)
                elif char.islower():
                    obfuscated += chr((ord(char) - ord('a') + 13) % 26 + ord('a'))
                elif char.isupper():
                    obfuscated += chr((ord(char) - ord('A') + 13) % 26 + ord('A'))
                else:
                    obfuscated += char
            else:
                obfuscated += char
        
        return obfuscated
    
    @staticmethod
    def deobfuscate_string(obfuscated_text: str) -> str:
        """字符串反混淆"""
        if not obfuscated_text:
            return obfuscated_text
        
        # 反向字符替换
        deobfuscated = ""
        for char in obfuscated_text:
            if char.isalnum():
                if char.isdigit():
                    deobfuscated += str((int(char) - 5) % 10)
                elif char.islower():
                    deobfuscated += chr((ord(char) - ord('a') - 13) % 26 + ord('a'))
                elif char.isupper():
                    deobfuscated += chr((ord(char) - ord('A') - 13) % 26 + ord('A'))
                else:
                    deobfuscated += char
            else:
                deobfuscated += char
        
        return deobfuscated
    
    @staticmethod
    def encode_email(email: str) -> str:
        """邮箱地址编码（防爬虫）"""
        if not email or '@' not in email:
            return email
        
        # 简单的字符替换
        encoded = email.replace('@', '[at]').replace('.', '[dot]')
        return encoded
    
    @staticmethod
    def decode_email(encoded_email: str) -> str:
        """邮箱地址解码"""
        if not encoded_email:
            return encoded_email
        
        # 反向替换
        decoded = encoded_email.replace('[at]', '@').replace('[dot]', '.')
        return decoded
    
    @staticmethod
    def mask_sensitive_data(data: str, mask_char: str = '*', keep_start: int = 2, keep_end: int = 2) -> str:
        """敏感数据脱敏"""
        if not data or len(data) <= keep_start + keep_end:
            return data
        
        start = data[:keep_start]
        end = data[-keep_end:] if keep_end > 0 else ""
        middle = mask_char * (len(data) - keep_start - keep_end)
        
        return start + middle + end
    
    @staticmethod
    def generate_token(length: int = 32) -> str:
        """生成访问令牌"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def hash_password(password: str, salt: str = None) -> Dict[str, str]:
        """密码哈希"""
        if salt is None:
            salt = secrets.token_hex(16)
        
        # 使用PBKDF2进行密码哈希
        import hashlib
        
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000  # 迭代次数
        )
        
        return {
            'hash': password_hash.hex(),
            'salt': salt
        }
    
    @staticmethod
    def verify_password(password: str, password_hash: str, salt: str) -> bool:
        """验证密码"""
        computed_hash = Crypto.hash_password(password, salt)['hash']
        return computed_hash == password_hash
