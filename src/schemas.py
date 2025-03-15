register_schema = {
    'username': {
        'type': 'string', 'minlength': 3, 'maxlength': 50, 'required': True
    },
    'password': {
        'type': 'string', 'minlength': 8, 'maxlength': 50, 'required': True
    },
    'email': {
        'type': 'string', 'regex': r'.*@.*\.com', 'required': True
    },
    'cpf': {
        'type': 'string', 'regex': r'\d{3}\.\d{3}\.\d{3}-\d{2}', 'required': True
    },
    'phone': {
        'type': 'string', 'regex': r'^\(\d{2}\) \d{4,5}-\d{4}$', 'required': True
    },
    'cep': {
        'type': 'string', 'regex': r'\d{5}-\d{3}', 'required': True
    },
    'street': {
        'type': 'string', 'maxlength': 100, 'required': True
    },
    'number': {
        'type': 'string', 'maxlength': 10, 'required': True
    },
    'complement': {
        'type': 'string', 'maxlength': 50, 'required': False
    },
    'city': {
        'type': 'string', 'maxlength': 50, 'required': True
    },
    'state': {
        'type': 'string', 'regex': r'^[A-Z]{2}$', 
        'allowed': ['AC','AL','AP','AM','BA','CE','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO'], 
        'required': True
    },
    'role': {
        'type': 'string', 'allowed': ['user', 'master'], 'default': 'user'
    },
    'token': {
        'type': 'string', 'required': False
    },
    'attempts': {
        'type': 'integer', 'min': 0, 'default': 0
    },
    'blocked': {
        'type': 'boolean', 'default': False
    }
}