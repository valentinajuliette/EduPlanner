# EduPlanner

## ESPECIFICACIÓN DEL PROYECTO
En este certamen los estudiantes en grupos de máximo dos integrantes deberán construir un sitio web
basado en Django Framework que solucione el problema planteado en el caso.

**Objetivos:**
  1. Desarrollar aplicaciones que promuevan el desacoplamiento entre sus componentes utilizando un
  modelo de capas.
  2. Desarrollar programas que permitan presentar y modificar información interactuando con bases de
  datos.
  3. Desarrollar programas que realicen llamadas a servicios externos invocando APIs REST.

## Descripción del caso
El proyecto "EduPlanner" se enfoca en la creación de una aplicación web que ayuda a instituciones educativas
y estudiantes a planificar y gestionar sus actividades académicas y personales. La aplicación se alimenta de
una API de terceros para obtener información sobre los feriados de Chile y cuenta con un sistema web que
permite a los distintos actores del sistema educativo (como administradores académicos, docentes y
personal de servicios estudiantiles) publicar actividades importantes. Estas actividades pueden incluir
períodos académicos, fechas de exámenes, plazos para solicitudes y gestión de beneficios, entre otros.
**Objetivo:** Implementar un sistema que centralice y unifique todas estas fuentes de información en un
calendario académico, sirviendo como puente de comunicación entre los datos ingresados por distintos
actores y EduPlanner. Este sistema debe exponer la información a través de una API pública en formato JSON
para que pueda ser consumida por aplicaciones como EduPlanner.

### Componentes del Sistema:
  1. Integración con una API de Terceros (Calendarific o similar):
    • Obtener y actualizar información sobre los feriados en Chile, incluyendo feriados nacionales,
  regionales y otros días no laborables.
  2. Desarrollo de una API Propia con Django REST Framework:
    • Crear una API que permita a las instituciones publicar actividades académicas (inicio y fin de períodos,
  plazos de solicitudes, fechas de exámenes, etc.).
    • Integrar la información de los feriados de la API de terceros con los eventos publicados por las
  instituciones.
    • La API debe exponer un calendario académico consolidado en formato JSON, que pueda ser
  fácilmente consumido por EduPlanner u otras aplicaciones.
  3. Sistema Web para la Gestión de Actividades:
    • Desarrollar un panel de administración donde los actores del sistema educativo puedan ingresar,
  modificar y eliminar eventos académicos.
    • Implementar funcionalidades de autenticación y roles para garantizar que solo usuarios autorizados
  puedan publicar o modificar actividades.
    • Permitir la visualización previa del calendario consolidado para verificar que las actividades y los
  feriados no se superpongan.
### Requerimientos Funcionales:
  • El sistema debe permitir la creación de eventos académicos con detalles como título, descripción,
  fecha de inicio y fin.
  • La API debe fusionar los eventos académicos con los feriados obtenidos de la API de terceros y
  devolver un calendario ordenado cronológicamente.
  • Los usuarios deben poder filtrar eventos por tipo (feriado, examen, plazo administrativo, etc.).
  • Implementar notificaciones automáticas para advertir sobre posibles conflictos entre eventos y
  feriados.

## ANEXOS
### Anexo 1: Reglas del Negocio

**Regla de Publicación de Eventos:**
  • Solo los usuarios con roles de administrador académico pueden publicar, modificar o eliminar
  eventos académicos en el sistema. Los estudiantes y otros usuarios solo tendrán permisos de lectura
  sobre el calendario académico.
  
**Regla de Prioridad de Eventos:**
  • En caso de conflicto entre un evento académico y un día no laborable (feriado), el sistema debe
  enviar una alerta al administrador indicando el conflicto. El administrador decidirá si se reprograma
  el evento o se mantiene la fecha con una nota explicativa.
  
**Regla de Formato de Eventos:**
  • Todos los eventos académicos deben incluir un título, descripción, fecha de inicio y fin, y un tipo de
  evento (por ejemplo, examen, plazo de solicitud, inicio de semestre). Los eventos sin estos datos
  completos no podrán ser publicados.

**Regla de Accesibilidad al Calendario:**
  • El calendario académico completo debe estar disponible públicamente a través de la API en formato
  JSON. Los datos confidenciales, como eventos internos de planificación, solo deben ser visibles para
  usuarios autorizados.

**Regla de Verificación y Aprobación:**
  • Antes de publicar un evento que afecte a múltiples usuarios (como un examen o un inicio de
  semestre), este debe pasar por una etapa de revisión y aprobación por parte del comité académico.
  Una vez aprobado, el evento se marcará como "oficial" y se publicará en el calendario.

El listado de tipos de eventos que podrían ser utilizados en el proyecto "EduPlanner":

  1. Inicio de Semestre: Fecha en la que comienza un nuevo período académico.

  2. Fin de Semestre: Fecha en la que termina el período académico.
  
  3. Inicio de Inscripción de Asignaturas: Fecha en la que se abre el período de inscripción de asignaturas
  para los estudiantes.
  
  4. Fin de Inscripción de Asignaturas: Fecha en la que se cierra el período de inscripción de asignaturas.
  
  5. Receso Académico: Período de vacaciones o receso sin actividades académicas.
  
  6. Feriado Nacional: Día no laborable reconocido a nivel nacional.
  
  7. Feriado Regional: Día no laborable específico de una región o localidad.
  
  8. Inicio de Plazos de Solicitudes Administrativas: Fecha de inicio para la realización de solicitudes
  como retiros de asignaturas, cambios de carrera, etc.
  
  9. Fin de Plazos de Solicitudes Administrativas: Fecha de cierre para la realización de dichas solicitudes.
  
  10. Inicio de Plazos para la Gestión de Beneficios: Fecha en la que se abre el período de postulación o
  renovación de beneficios estudiantiles.
  
  11. Fin de Plazos para la Gestión de Beneficios: Fecha de término del período de postulación o
  renovación de beneficios.
  
  12. Ceremonia de Titulación o Graduación: Fecha de la ceremonia de titulación para estudiantes que
  completaron su plan de estudios.
  
  13. Reunión de Consejo Académico: Fecha de reuniones importantes del consejo académico o
  comisiones de evaluación.
  
  14. Talleres y Charlas: Eventos de formación y desarrollo profesional organizados por la institución.
  
  15. Día de Orientación para Nuevos Estudiantes: Evento de bienvenida y orientación para estudiantes
  de primer ingreso.
  
  16. Eventos Extracurriculares: Fechas de actividades extracurriculares como competiciones deportivas,
  presentaciones artísticas o ferias.
  
  17. Inicio de Clases: Fecha de inicio de las clases después de un receso académico o vacaciones.
  
  18. Último Día de Clases: Último día oficial de clases antes de los exámenes o recesos.
  
  19. Día de Puertas Abiertas: Evento en el que la institución recibe visitantes para conocer sus programas
  académicos y servicios.
  
  20. Suspensión de Actividades Completa: Período en el que todas las actividades académicas y
  administrativas se suspenden en la institución debido a situaciones especiales como celebraciones
  internas, emergencias climáticas o motivos de fuerza mayor.
  
  21. Suspensión de Actividades Parcial: Período en el que se suspenden ciertas actividades académicas
  o administrativas, afectando solo a una parte de la institución o a ciertos grupos específicos (por
  ejemplo, un departamento en particular).
