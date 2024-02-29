---
title: Código con forma de donut que produce un donut.
subtitle: Código con forma de donut que produce un donut tridimensional en rotación.
---

Hay una imagen que ha rondado mi cabeza desde que la vi hace años. ["Donut-shaped C code that generates a 3D spinning donut"](https://www.youtube.com/watch?v=DEqXNfs_HhY) fue, si no me equivoco, el vídeo donde la vi por primera vez. Durante mucho tiempo esta pieza de código me antojaba mágica. Incluso tras deshacer su forma toroidal me resultaba imposible interpretar ese conjunto caótico de variables sin significado semántico. Nunca llegué a darle la importancia ni la atención que merecía, pues pensaba que era simplemente un juego intelectual entre programadores.

Hace dos días sin embargo me obsesioné con el tema y, tras unas tres tardes de álgebra lineal y Python, vi que era en realidad sorprendentemente sencillo. Mi objetivo no ha sido llegar a algo si quiera remotamente similar a aquél código, sino más bien experimentar con las matemáticas involucradas desde cero. He procurado no leer absolutamente nada sobre cómo funciona la iluminación ni las proyecciones, y obviamente no ha quedado un resultado perfecto, pero ha sido una experiencia muy interesante.

# 1. Objetivo

El objetivo final es sencillo: mostrar un donut tridimensional bailando en la terminal. Atacar un problema así partiendo desde la perspectiva de los algoritmos tiende a resultar en código enrevesado o ineficiente, así que vamos a trabajar como si los ordenadores no existiesen - con matemáticas. Podemos descomponer el problema en otros cinco bastante más sencillos:

1. Describir los puntos de un donut (o "toro") usando ecuaciones paramétricas.
2. Hacer "bailar" al donut utilizando matrices.
3. Asociar a cada punto del donut un valor de luminosidad.
4. Proyectar los puntos del donut a un plano bidimensional.
5. Pasar del plano a la terminal y mostrar el donut.

Después, escribiremos el código respectivo en Python y finalmente lo transferiremos a C, donde lo reduciremos a su mínima expresión y le daremos forma de donut.

# 2. El donut

Las ecuaciones paramétricas que describen a un toro centrado en el eje z son las siguientes:

$$x = \cos(u) (R + r \cos(v))$$
$$y = \sin(u) (R + r \cos(v))$$
$$z = r \sin(v)$$

_(Inicialmente busqué estas ecuaciones, pero después me di cuenta de que son el resultado de aplicar una matriz de rotación a una circunferencia desfasada del origen. No es importante, pero me dio una grata sorpresa)_

![(Figura 1) $u$ y $v$ describiendo los puntos del toro.](https://web.maths.unsw.edu.au/~rsw/Torus/torus1.jpg)

Transferir esto a código es trivial. Dentro de la clase `Torus` tenemos el siguiente método:

~~~~py
class Torus
def point_at(self, u, v):
	x = np.cos(u) * (self.R + self.r * np.cos(v))
	y = np.sin(u) * (self.R + self.r * np.cos(v))
	z = self.r * np.sin(v)

	return np.array([x, y, z])
~~~~

En primera instancia podría resultar arbitrario centrar el toro en torno al eje Z, sin embargo cuando apliquemos las rotaciones esto no influirá.

# 3. El baile

Dado cualquier punto del donut, podemos aplicarle transformaciones lineales a través de matrices. No nos interesa nada demasiado sofisticado, así que con unas rotaciones sencillas bastará. El ángulo $\theta$ irá variando para generar el efecto de movimiento.

$$
\begin{pmatrix}
1 & 0 & 0 \\
0 & \cos(\theta) & -\sin(\theta) \\
0 & \sin(\theta) & \cos(\theta)
\end{pmatrix}
$$

También podemos mover el donut de arriba a abajo muy ligeramente:

$$y(\theta) = \cos(\theta)$$

# 4. La luz

Determinar el brillo de un punto del toro sería extremadamente sencillo de no ser por la existencia de sombras. Como el plan es resolver esto rápidamente y sin consultar recursos externos, ignoraremos este problema.

En esencia, si un rayo de luz impacta perpendicularmente sobre una superficie, esta alcanzará su luminosidad máxima. Cuanto más "inclinado" esté este ángulo, más oscura será la superficie.

Un sinónimo a esto es preguntarse cómo de alineados están el vector normal a la superficie con el vector desde la fuente de luz hasta la superficie. (Figura 2)

![(Figura 2) Cuanto menor sea el ángulo formado entre $N$ y $L-P$, mayor será el valor de brillo de ese punto.](/static/articles_media/donut/light_source.png)

La operación por excelencia para hallar cómo de alineados están dos vectores es el producto escalar, y para obtener valores de brillo que estén entre 0 y 1 (incluídos), debemos normalizar antes los vectores.

$$\vec{V} = L - P$$
$$\vec{v} = \frac{\vec{V}}{\mid \vec{V} \mid}$$
$$\textrm{brillo} = \vec{v} \cdot \vec{N}$$

Solo nos queda obtener la normal a la superficie de un punto del toro. Si imaginamos desplazarnos un pequeño paso en $u$ (es decir, $\textrm{toro}(u + du, v)$), estaremos en un nuevo punto. Cabe notar que si damos el mismo paso pero en $v$ (es decir, $\textrm{toro}(u, v + dv)$), nos moveremos perpendicularmente respecto de la dirección anterior. Esto es valioso, pues con ambas direcciones definimos un plano tangente a la superficie del toro, y obtener la normal de este plano es sencillo.

Antes de hacerlo podemos formalizar a qué nos referimos al decir "un pequeño paso". Lo que en realidad estamos haciendo es calcular las derivadas de las ecuaciones paramétricas respecto de $u$ y de $v$ en todas las coordenadas, es decir:

$$\frac{dx}{du} = \frac{d}{du}(\cos(u)(R + r\cos(v))$$
$$\frac{dy}{du} = \frac{d}{du}(\sin(u)(R + r\cos(v)))$$
$$\frac{dz}{du} = \frac{d}{du}(r\sin(v))$$
$$\\$$
$$\frac{dx}{dv} = \frac{d}{dv}(\cos(u)(R + r\cos(v))$$
$$\frac{dy}{dv} = \frac{d}{dv}(\sin(u)(R + r\cos(v)))$$
$$\frac{dz}{dv} = \frac{d}{dv}(r\sin(v))$$

Este conjunto nos dará dos vectores, llamémoslos $\frac{d\vec{V}}{du}$ y $\frac{d\vec{V}}{dv}$. Como hemos dicho, estos vectores son ortogonales entre sí y pertenecen al plano tangente a la superficie del donut en ese punto, por lo que su producto vectorial nos dará otro vector perpendicular a ambos.

¿Cómo decidimos en qué orden realizar este producto? Sinceramente no he encontrado un razonamiento para esta pregunta, así que he probado las dos formas y me he quedado con la que me diera un resultado coherente, en este caso:

$$\vec{N} = \frac{d\vec{V}}{dv} \times \frac{d\vec{V}}{du}$$

La función resultante que también normaliza los vectores es:

~~~py
class Torus
def normal_at(self, u, v):
	dV_du = np.array([-np.sin(u)*(torus.R + torus.r * np.cos(v)),
						np.cos(u)*(torus.R + torus.r * np.cos(v)),
						0])
	dV_dv = np.array([-torus.r*np.cos(u)*np.sin(v),
						-torus.r*np.sin(u)*np.sin(v),
						torus.r*np.cos(v)])
	normal = np.cross(dV_dv, dV_du)
	normal = normal / np.linalg.norm(normal)
	return normal
~~~

Al hallar el producto escalar $\vec{v} \cdot \vec{N}$, podemos obtener valores negativos, que simbolizarían que la superficie "da la espalda" a la fuente de luz, por ello interpretamos valores menores a cero como nulos. La función resultante es la siguiente:

~~~py
Brightness
def brightness_at(torus, u, v, rotation_matrix, light_source):
	point = rotation_matrix @ torus.point_at(u, v)
	normal = rotation_matrix @ torus.normal_at(u, v)
	d = light_source - point
	d = d / np.linalg.norm(d)

	brightness = np.dot(d, normal)

	if brightness < 0:
		return 0
	else:
		return brightness
~~~

# 5. La proyección

Dado un plano y un punto, la proyección del punto sobre el plano consistirá en moverlo perpendicular al plano hasta acabar sobre él. Para averiguar la distancia del punto al plano podemos crear un vector $\vec{v}$ que vaya del origen del plano hasta el punto deseado y hacer su producto escalar con la normal del plano. La proyección entonces será restar al punto la normal al plano escalada por la distancia. Esto consigue un movimiento perpendicular que lo deja exactamente sobre el plano.

~~~py
class Plane
def project(self, point):
	v = point - self.Origin
	distance = v.dot(self.Normal)
	projected_point = point - distance * self.Normal

	return projected_point
~~~

# 6. La terminal

En primer lugar estableceremos como sistema de referencia el origen del plano:

~~~py
class Plane
def relative_coords(self, point):
	return point - self.Origin
~~~

Nuestro sistema de referencia tiene al plano en el origen. Sin embargo el origen de coordenadas de la terminal está en la esquina superior izquierda, y avanza de arriba a abajo. Conociendo la cantidad de filas y columnas de la terminal, esto no es complicación:

~~~py
Terminal Coordinates
def plane_coords_to_terminal_coords(plane_coords):
	col = int(COLS/2 + plane_coords[0])
	row = int(ROWS/2 - plane_coords[2])

	return (row, col)

# main
projected_point = plane.project(torus_point)
projected_point = plane.relative_coords(projected_point)
(row, col) = plane_coords_to_terminal_coords(projected_point)
~~~

Ahora el procedimiento es obvio. Tomamos el brillo y le asignamos un caracter en una lista que represente cada posición en la terminal.

~~~py
def main()	
brightness = brightness_at(torus, u, v, rotation_matrix, light_source)
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

Como avisé al principio, no nos centraremos en perfeccionar este dato, aunque una solución que produce un resultado bastante decente es simplemente quedarse con el valor de brillo más alto encontrado.

# Resultado

¡Y ya está! El código completo está disponible en mi [GitHub](https://github.com/erikucenik/donut/blob/master/donut.py). No es una joya pero es lo que tiene la improvisación. Transformado a C y reducido lo máximo posible, lo podemos amasar hasta que sea un donut y... ¡listo!

Pasarlo a C es más tedioso que difícil, puesto que no contamos con las facilidades de NumPy y Python, pero nada imposible. El [código traducido](https://github.com/erikucenik/donut/blob/master/donut.c) se encuentra también en mi GitHub. Era de esperar, pero la diferencia en velocidad fue remarcable.

Sin embargo este código es demasiado largo para darle forma de donut, entonces es necesario simplificarlo. Es aquí donde hice una pequeña trampa, pues no solo me dediqué a agrupar y a cambiar nombres, sino que además recogí muchas funciones en el archivo [donut.h](https://github.com/erikucenik/donut/blob/master/donut.h).

Con este código reducido no queda más que eliminar los espacios innecesarios y moldear el código como si fuese un donut. Esto lo hice a ojo de buen cubero (no es necesario sofisticarlo todo). Para llenar los huecos utilicé unos cuantos comentarios, [et voilá](https://github.com/erikucenik/donut/blob/master/donut_shaped_c_code_that_generates_a_spinning_donut.c).

![*Habemus donut.*](/static/articles_media/donut/donut.png)

![*Fin.*](/static/articles_media/donut/donut.gif)
