from django import template

register = template.Library()

@register.filter(name='subtract')
def subtract(value, arg):
    return -(value - arg)   


# @register.filter(name='initial')
# def initial(value = 0):
#     return value

# @register.simple_tag(takes_context=True)
# def subtractify(context, obj):
#     newval = obj.loan_amount - obj.service_charge
#     return newval
 