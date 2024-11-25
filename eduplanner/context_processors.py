def verificar_autorizacion(request):
    if request.user.is_authenticated:
        # Comprobar si el usuario pertenece a los grupos 'Académicos' o 'Comité Académico'
        autorizacion = request.user.groups.filter(name__in=['Académicos', 'Comité Académico']).exists()
    else:
        autorizacion = False
    return {'autorizacion': autorizacion}