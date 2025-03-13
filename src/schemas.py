register_schema = {'username': {'type': 'string', 'minlength': 3, 'maxlength': 20, 'required': True},
                   'password': {'type': 'string', 'minlength': 8, 'maxlength': 20, 'required': True},
                   'email': {'type': 'string', 'regex': r'.*@.*\.com', 'required': True}}