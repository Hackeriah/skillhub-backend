from django.db import models
import bcrypt

# Custom User Model
class User(models.Model):
    firstname = models.CharField(max_length=150, unique=True)
    lastname = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        """Hashes the password using bcrypt and saves it."""
        self.password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, raw_password):
        """Compares raw password with hashed password."""
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))

    def __str__(self):
        return self.firstname + ' ' + self.lastname
