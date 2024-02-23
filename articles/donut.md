---
title: Código con forma de donut que produce un donut.
subtitle: Código con forma de donut que produce un donut tridimensional en rotación.
---

# DONUT

Hay una imagen que ha rondado mi cabeza desde que la vi hace años. "Donut-shaped C code that generates a 3D spinning donut - Lex Fridman" fue, si no me equivoco, el vídeo donde la vi por primera vez. Durante mucho tiempo esta pieza de código me antojaba mágica. Incluso tras deshacer su forma toroidal me resultaba imposible interpretar ese conjunto caótico de variables sin significado semántico. Nunca llegué a darle la importancia ni la atención que merecía, pues pensaba que era simplemente un juego intelectual entre programadores.

Hace dos días sin embargo me obsesioné con el tema, y tras unas tres tardes de álgebra lineal y Python, vi que conceptualmente era en realidad sorprendentemente sencillo. El objetivo de este texto no es replicar exactamente el código original, sino más bien explicar cómo se puede llegar hasta algo similar de manera que cada paso resulte evidente por sí mismo.

=====

El objetivo final es sencillo: mostrar un donut tridimensional bailando en la terminal. Atacar un problema así partiendo desde la perspectiva de los algoritmos tiende a resultar en código enrevesado o ineficiente, así que vamos a trabajar como si los ordenadores no existiesen - con matemáticas. Podemos descomponer el problema en otros cinco bastante más sencillos:

1. Describir los puntos de un donut (o "toro") usando ecuaciones paramétricas.
2. Hacer "bailar" al donut utilizando matrices.
3. Asociar a cada punto del donut un valor de luminosidad.
4. Proyectar los puntos del donut a un plano bidimensional.
5. Pasar del plano a la terminal y mostrar el donut.

Después, escribiremos el código respectivo en Python y finalmente lo transferiremos a C, donde lo reduciremos a su mínima expresión y le daremos forma de donut.

# 1. El donut

Las ecuaciones paramétricas que describen a un toro centrado en el eje z son las siguientes:

$$x = cos(\alpha) * (R + r*cos(\beta))$$
$$y = sin(\alpha) * (R + r*cos(\beta))$$
$$z = r * sin(\beta)$$

Uno puede pararse a imaginar un círculo de radio R en torno al eje Z en cuyo borde hay otro círculo de radio r. Los puntos del toro son entonces descritos por el ángulo alpha que forma un radio del primer círculo con el eje X y por el ángulo beta que forma otro radio del segundo círculo con la extensión del radio del primero. ¿Parece un trabalenguas? Es simplemente esta imagen:

https://web.maths.unsw.edu.au/~rsw/Torus/torus1.jpg

Es además bastante fácil transferir esto a código:

~~~~py
Punto del Toro
def point_at(self, alpha, beta):
	x = np.cos(alpha) * (self.R1 + self.R2 * np.cos(beta))
	y = np.sin(alpha) * (self.R1 + self.R2 * np.cos(beta))
	z = self.R2 * np.sin(beta)

	return np.array([x, y, z])
~~~~

En primera instancia podría resultar arbitrario centrar el toro en torno al eje Z, sin embargo cuando apliquemos las rotaciones esto no influirá.

# 2. El baile

Dado cualquier punto del donut, podemos aplicarle transformaciones lineales a través de matrices. No nos interesa nada demasiado sofisticado, así que con unas rotaciones sencillas bastará. El ángulo $\theta$ irá variando para generar el efecto de movimiento.

~~~py
Rotación
rotation_matrix_x = np.array([[1, 0, 0],
							[0, np.cos(theta), -np.sin(theta)],
							[0, np.sin(theta), np.cos(theta)]])
rotation_matrix_y = np.array([[np.cos(theta), 0, np.sin(theta)],
							[0, 1, 0],
							[-np.sin(theta), 0, np.cos(theta)]])

rotation_matrix = y_rotation_matrix @ x_rotation_matrix
point = rotation_matrix @ torus.point_at(0, 3.14)
~~~

También podemos mover el donut de arriba a abajo muy ligeramente con la siguiente línea:

~~~py

point += np.array([0, np.cos(theta), 0])
~~~

# 3. La luz

Determinar cómo de brillante es un punto del toro es conceptualmente sencillo, aunque algo largo visto en código. En esencia, dadas las coordenadas de una fuente de luz, el ángulo que forme el vector normal de una superficie con el vector que la une con dicha fuente determinará la luminosidad. De nuevo, suena más complicado de lo que realmente es. Lo que estamos midiendo es cómo de perpendicular es la superficie a la fuente de luz: si la encara totalmente, alcanzará su máximo brillo, si está ligeramente inclinada, no será tan intenso, y si "se dan la espalda", el brillo será nulo.

Empecemos primero por obtener la normal a la superficie del toro dado un punto `toro(alpha, beta)`. Si imaginamos desplazarnos un pequeño paso en alpha (es decir, `toro(alpha + da, beta)`), estaremos en un nuevo punto. Cabe notar que si damos el mismo paso pero en beta (es decir, `toro(alpha, beta + db)`), nos moveremos perpendicularmente respecto de la dirección anterior. Esto es valioso, pues con ambas direcciones definimos un plano tangente a la superficie del toro, y obtener la normal de este plano es sencillo.

Antes de ello podemos formalizar a qué nos referimos al decir "un pequeño paso". Lo que en realidad estamos diciendo es tomar las derivadas de las ecuaciones paramétricas respecto de alpha y de beta en todas las coordenadas, es decir:

$$\frac{dx}{d\alpha} = \frac{d}{dx}(cos(\alpha) * (R + r*cos(\beta)))$$
$$\frac{dx}{d\beta} = \frac{d}{dx}(cos(\alpha) * (R + r*cos(\beta)))$$
$$\frac{dy}{d\alpha} = \frac{d}{dx}(cos(\alpha) * (R + r*cos(\beta)))$$
$$\textrm{etc.}$$

Este conjunto nos dará dos vectores, llamémoslos $$\frac{d\vec{v}}{d\alpha}$$ y $$\frac{d\vec{v}}{d\beta}$$. Como hemos dicho, estos vectores son perpendiculares y pertenecen al plano tangente a la superficie del donut en ese punto, por lo que su producto vectorial nos dará otro vector perpendicular a ambos. ¿Cómo decidimos en qué orden realizar este producto? Sinceramente no he encontrado un razonamiento para esta pregunta, así que he probado las dos formas y me he quedado con la que me diera un resultado coherente. La función resultante es:

~~~py
Normal
def get_normal(torus, alpha, beta):
	dv_da = np.array([-np.sin(alpha)*(torus.R1 + torus.R2 * np.cos(beta)),
						np.cos(alpha)*(torus.R1 + torus.R2 * np.cos(beta)),
						0])
	dv_db = np.array([-torus.R2*np.cos(alpha)*np.sin(beta),
						-torus.R2*np.sin(alpha)*np.sin(beta),
						torus.R2*np.cos(beta)])
	normal = np.cross(dv_db, dv_da)
	normal = normal / np.linalg.norm(normal)
	return normal
~~~

Ahora sí, podemos calcular el brillo de cualquier punto. Solo necesitamos crear un vector `d` desde el punto hasta la fuente de luz. Habiéndolos normalizado, medir cómo de alineados están `d` y la normal a la superficie del toro se puede hacer realizando su producto escalar. El valor resultante será 0 si son perpendiculares, un número negativo si están alineados en distintas direcciones, y un valor positivo si lo están en la misma dirección. De hecho nos interesa revertir estos dos últimos casos, ya que de estar alineados significaría que la superficie "da la espalda" a la fuente de luz y no está iluminada. Añadimos entonces un signo menos en frente del vector perpendicular. De obtener un valor negativo, lo interpretaremos como brillo nulo. 

La función resultante es la siguiente:

~~~py
Brightness
def get_brightness(torus, alpha, beta, rotation_matrix, light_source):
	normal = get_normal(torus, alpha, beta)
	point = rotation_matrix @ torus.point(alpha, beta)
	point += np.array([0, np.cos(theta), 0])
	normal = rotation_matrix @ get_normal(torus, alpha, beta)
	d = point - light_source
	d = d / np.linalg.norm(d)

	brightness = np.dot(d, -normal)

	if brightness < 0:
		return 0
	else:
		return brightness
~~~

# 4. La proyección

Dado un plano y un punto, la proyección del punto sobre el plano consistirá en moverlo perpendicular al plano hasta acabar sobre él. Para averiguar la distancia del punto al plano podemos crear un vector `v` que vaya del origen del plano hasta el punto deseado y hacer su producto escalar con la normal del plano. La proyección entonces será restar al punto la normal al plano escalada por la distancia. Esto consigue un movimiento perpendicular que lo deje exactamente sobre el plano.

~~~py
class Plane
def project(self, point):
	v = point - self.Origin
	distance = v.dot(self.Normal)
	projected_point = point - distance * self.Normal

	return projected_point
~~~

# 5. La terminal

En primer lugar estableceremos como sistema de referencia el origen del plano:

~~~py
Coords
def relative_coords(self, point):
	return point - self.Origin
~~~

Ahora nuestro sistema de referencia tiene al plano en el origen. Sin embargo el origen de coordenadas de la terminal está en la esquina superior izquierda, y avanza de arriba a abajo. Conociendo la cantidad de filas y columnas de la terminal, esto no es complicación:

~~~py
Projection
projection = plane.project(point)
coords_in_plane = plane.relative_coords(projection)
col = int(COLS/2 + coords_in_plane[0])
row = int(ROWS/2 - coords_in_plane[1])
~~~

Ahora el procedimiento es obvio. Tomamos el brillo y le asignamos un caracter en una lista que represente cada posición en la terminal.

~~~py

brightness = get_brightness(torus, alpha, beta, rotation_matrix, light_source, theta)
character = brightness_to_character(brightness)
screen[row][col] = character
~~~

La función que asocie un caracter a cada brillo puede decidirse libremente, pero me voy a remitir al conjunto de caracteres original.

~~~py
Bright2Char
def brightness_to_character(brightness):
	# brightness -> [0..1]
	# characters -> [0..11]
	index = round(brightness*11)
	characters = ".,-~:;=!*#$@"
	return characters[index]
~~~

En realidad hay un último detalle a considerar. Distintos puntos del donut con distintas luminosidades pueden ser proyectados al mismo lugar en la terminal, determinando el resultado en función del orden en que hayan sido escritos y no en la figura tridimensional.

La verdadera solución a este problema sería tomar el brillo del punto del toro más cercano al plano, pero una solución más sencilla y que produce un resultado bastante decente es simplemente quedarse con el valor de brillo más alto encontrado.

~~~py

brightness = get_brightness(torus, alpha, beta, rotation_matrix, light_source, theta)
new_character = brightness_to_character(brightness)

try:
	old_index = ".,-~:;=!*#$@".index(screen[row][col])
	new_index = ".,-~:;=!*#$@".index(new_character)
	
	if new_index > old_index:
		screen[row][col] = new_character
			
except ValueError:
	screen[row][col] = new_character
~~~

# Resultado

¡Y ya está! El código completo está disponible en mi GitHub. No es una joya pero es lo que tiene la improvisación. Transformado a C y reducido lo máximo posible, lo podemos amasar hasta que sea un donut y... ¡listo!

Pasarlo a C será más tedioso que difícil, puesto que no contamos con las facilidades de NumPy y Python, pero nada imposible. El código traducido se encuentra también en mi GitHub. Era de esperar, pero la diferencia en velocidad fue remarcable.

Sin embargo este código es demasiado largo para darle forma de donut, entonces es necesario simplificarlo. Es aquí donde hice una pequeña trampa, pues no solo me dediqué a agrupar y a cambiar nombres, sino que además recogí muchas funciones en el archivo "donut.h".

Con este código reducido no queda más que eliminar los espacios innecesarios y moldear el código como si fuese un donut. Esto lo hice a ojo de buen cubero (no es necesario sofisticarlo todo). Para llenar los huecos utilicé unos cuantos comentarios et voilá.

=====

Publicar en una página web que me haga. Utilizar los dos primeros párrafos para un post de linkedin que redireccione a esta página web. Publicar el código también en github y redireccionar a ese github. 
