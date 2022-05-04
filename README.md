# Django-Project-Storeproject


## reset-password setting
add Email and Password at `.\Django-Project-Storeproject\django48_1_5\django48_1_5\settings.py`,
Email is lesssecure -> https://myaccount.google.com/lesssecureapps
```
EMAIL_HOST_USER = '** eamil **'
EMAIL_HOST_PASSWORD = '** password email **'
```
---
edit django at `.\django-tictactoe-AI\env\Lib\site-packages\django\contrib\admin\templates\registration\password_reset_email.html'
### Old
```
{{ protocol }}://{{ domain }}{% url 'password_reset_confirm' uidb64=uid token=token %}
```
### New
```
{{ protocol }}://{{ domain }}{% url 'myapp:password_reset_confirm' uidb64=uid token=token %}
```
---

### Requirements
```
django
django-crispy-forms
crispy-bootstrap5
pillow
```
