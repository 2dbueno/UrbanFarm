# templatetags/custom_filters.py
from django import template
import re
register = template.Library()

@register.filter
def format_cnpj(cnpj):
    if len(cnpj) == 14:  # Certifica-se de que o CNPJ tem 14 dígitos
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
    return cnpj  # Retorna o CNPJ sem formatação se não tiver 14 dígitos

@register.filter
def format_cpf(cpf):
    if len(cpf) == 11:  # Certifica-se de que o CPF tem 11 dígitos
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return cpf  # Retorna o CPF sem formatação se não tiver 11 dígitos

@register.filter
def remove_format(cpf):
    return re.sub(r'\D', '', cpf)  # Remove todos os caracteres não numéricos