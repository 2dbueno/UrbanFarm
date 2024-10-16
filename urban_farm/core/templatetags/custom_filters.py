# templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def format_cnpj(cnpj):
    if len(cnpj) == 14:  # Certifica-se de que o CNPJ tem 14 dígitos
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
    return cnpj  # Retorna o CNPJ sem formatação se não tiver 14 dígitos
