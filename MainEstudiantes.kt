/**
 * MainEstudiantes.kt ("versión estudiante")
 * ==========================================
 * Hola! Este archivo lo escribí intentando ENTENDER (más que impresionar) cómo
 * funciona el algoritmo de Dijkstra en un grafo pequeño. Está TODO en un solo
 * archivo para no marearme cambiando de pestaña 😅.
 *
 * ¿Qué hay aquí? (mini índice)
 * 1. Defino el grafo como un Map simple: nodo -> lista de (vecino, peso)
 * 2. Implemento Dijkstra paso a paso (con prints opcionales para ver qué hace)
 * 3. Función para reconstruir la ruta usando un mapa de padres
 * 4. Un menú súper básico por consola
 * 5. Al iniciar, corre un ejemplo (A -> D) para que ya veas algo
 * 6. Extras: función para explicar el algoritmo y lista de retos al final
 *
 * NOTAS PERSONALES / COSAS QUE APRENDÍ:
 * - El "peso" aquí lo trato como "minutos".
 * - Uso PriorityQueue porque Dijkstra necesita siempre el nodo con menor distancia pendiente.
 * - El mapa de "padres" es CLAVE para reconstruir la ruta (sin eso solo sabría distancias).
 * - Int.MAX_VALUE lo uso como "infinito" (porque Kotlin no tiene un infinito entero nativo).
 *
 * DIAGRAMA (no está perfecto, pero me ayuda):
 *   A --15--> B --25--> D --10--> E --5--> F --8--> G
 *   |  \10    \                \10      \12
 *   |   \      \                --> F     --> G
 *   |    20      12
 *   v      \      
 *   C --12--> D
 *   | \15
 *   |  \30
 *   v    v
 *   F    E
 *
 * COMPILAR / EJECUTAR (opciones):
 *   kotlinc MainEstudiantes.kt -include-runtime -d rutas.jar && java -jar rutas.jar
 *   # o
 *   kotlinc MainEstudiantes.kt -d rutas.jar && java -cp rutas.jar MainEstudiantesKt
 *   # o (dependiendo de tu instalación)
 *   kotlin MainEstudiantes.kt
 *
 * SI TE PIERDES: baja hasta la función main() y lee para arriba.
 * Si quieres practicar, llama a la función retos() desde main.
 */

import java.util.PriorityQueue

// ---------------------------------------------------------------------------
// 1. DEFINICIÓN DEL GRAFO
// ---------------------------------------------------------------------------
// Mapa: cada nodo -> lista de (vecino, peso en minutos)
// Diseñado para que A->D = 32 y B->E = 27
val GRAFO: Map<String, List<Pair<String, Int>>> = mapOf(
    "A" to listOf("B" to 15, "C" to 20, "F" to 35),
    "B" to listOf("D" to 25, "C" to 10, "E" to 27),
    "C" to listOf("D" to 12, "F" to 15, "E" to 30),
    "D" to listOf("E" to 10, "F" to 10),
    "E" to listOf("F" to 5, "G" to 12),
    "F" to listOf("G" to 8),
    "G" to emptyList()
)

val NOMBRES: Map<String, String> = mapOf(
    "A" to "Aeropuerto",
    "B" to "Terminal",
    "C" to "Simón Bolívar",
    "D" to "Museo del Oro",
    "E" to "Monserrate",
    "F" to "Zona T",
    "G" to "EAN"
)

// ---------------------------------------------------------------------------
// 2. ALGORITMO DE DIJKSTRA (EXPLICADO)
// ---------------------------------------------------------------------------
/**
 * Calcula distancias mínimas desde [origen] a todos los nodos.
 * @param verPasos si es true imprime cada intento de relajación.
 * @return Pair(distancias, padres)
 */
fun dijkstra(
    grafo: Map<String, List<Pair<String, Int>>>,
    origen: String,
    verPasos: Boolean = false
): Pair<MutableMap<String, Int>, MutableMap<String, String?>> {

    // Dijkstra en una frase (mi resumen):
    // "Voy expandiendo siempre el camino más corto conocido y veo si puedo mejorar
    // (relajar) las distancias a los vecinos".

    // 1. Inicializamos distancias en infinito, excepto el origen
    val distancias = mutableMapOf<String, Int>()
    val padres = mutableMapOf<String, String?>()
    for (n in grafo.keys) {
        distancias[n] = Int.MAX_VALUE
        padres[n] = null
    }
    distancias[origen] = 0

    // 2. Cola de prioridad (menor distancia primero)
    data class Estado(val dist: Int, val nodo: String)
    val cola = PriorityQueue<Estado>(compareBy { it.dist })
    cola.add(Estado(0, origen))

    if (verPasos) println("\n[INICIO DIJKSTRA]")

    while (cola.isNotEmpty()) { // Mientras queden candidatos
        val actual = cola.poll()
        val nodo = actual.nodo
        val distActual = actual.dist

        if (verPasos) println("Procesando nodo $nodo con distancia $distActual")

        // Si ya tenemos algo mejor, saltamos
        if (distActual > distancias[nodo]!!) continue

        // Revisar vecinos (aquí ocurre la "relajación")
        for ((vecino, peso) in grafo[nodo] ?: emptyList()) {
            val nuevaDist = distActual + peso
            if (verPasos) println("  Vecino $vecino: actual=${distancias[vecino]} nueva=$nuevaDist")

            if (nuevaDist < distancias[vecino]!!) {
                distancias[vecino] = nuevaDist
                padres[vecino] = nodo
                cola.add(Estado(nuevaDist, vecino))
                if (verPasos) println("    Actualizado $vecino -> $nuevaDist (padre=$nodo)")
            }
        }
    }

    if (verPasos) println("[FIN DIJKSTRA]\n")

    return distancias to padres
}

// ---------------------------------------------------------------------------
// 3. RECONSTRUCCIÓN DE RUTA
// ---------------------------------------------------------------------------
fun reconstruirRuta(
    padres: Map<String, String?>,
    origen: String,
    destino: String
): List<String>? {
    // Si no tiene padre y no es el origen -> no hay ruta.
    if (padres[destino] == null && destino != origen) return null
    val ruta = mutableListOf<String>()
    var actual: String? = destino
    while (actual != null) {
        ruta.add(actual)
        actual = padres[actual]
    }
    ruta.reverse()
    return if (ruta.first() == origen) ruta else null
}

// Explicación breve imprimible (la puedo llamar desde el menú si quiero)
fun explicarDijkstraBreve() {
    println("\nExplicación rapida de Dijkstra (versión estudiante):")
    println("1. Empiezo con distancia 0 en el origen y ∞ en los demás.")
    println("2. Siempre tomo el nodo pendiente con menor distancia.")
    println("3. Intento mejorar (relajar) a cada vecino: dist[nuevo] = dist[actual] + peso.")
    println("4. Si mejoro una distancia, guardo quién fue su 'padre'.")
    println("5. Repito hasta que no hay nodos en la cola.")
    println("6. Para reconstruir la ruta: voy desde el destino hacia atrás usando padres[].")
}

// ---------------------------------------------------------------------------
// 4. UTILIDADES INTERACTIVAS
// ---------------------------------------------------------------------------
fun mostrarUbicaciones() {
    println("\nUbicaciones disponibles:")
    for (k in GRAFO.keys.sorted()) {
        println("  $k - ${NOMBRES[k]}")
    }
}

fun opcionRutaMasCorta() {
    mostrarUbicaciones()
    print("\nOrigen: ")
    val origen = readLine()?.trim()?.uppercase() ?: return
    print("Destino: ")
    val destino = readLine()?.trim()?.uppercase() ?: return

    if (!GRAFO.containsKey(origen) || !GRAFO.containsKey(destino)) {
        println(" Nodo inválido")
        return
    }

    print("¿Ver pasos internos de Dijkstra? (s/N): ") // Recomiendo probar 's' al menos una vez
    val ver = readLine()?.trim()?.lowercase() == "s"

    val (dist, padres) = dijkstra(GRAFO, origen, verPasos = ver)
    val ruta = reconstruirRuta(padres, origen, destino)

    if (ruta == null) {
        println("No existe ruta")
        return
    }

    println("\nResultado:")
    println("  Ruta: ${ruta.joinToString(" -> ")}")
    println("  Tiempo total: ${dist[destino]} minutos")

    // Tabla de segmentos
    println("\nSegmentos (para entender qué suma cada tramo):")
    var acumulado = 0
    for (i in 0 until ruta.size - 1) {
        val a = ruta[i]
        val b = ruta[i + 1]
        val peso = GRAFO[a]!!.first { it.first == b }.second
        acumulado += peso
        println("  $a -> $b: $peso (acumulado: $acumulado)")
    }
}

fun opcionTodasLasDistancias() {
    mostrarUbicaciones()
    print("\nOrigen: ")
    val origen = readLine()?.trim()?.uppercase() ?: return
    if (!GRAFO.containsKey(origen)) {
        println("Nodo inválido")
        return
    }
    val (dist, padres) = dijkstra(GRAFO, origen)
    println("\nDistancias mínimas desde $origen:")
    for (n in GRAFO.keys.sorted()) {
        val d = dist[n]
        val ruta = reconstruirRuta(padres, origen, n)
        if (ruta != null) {
            println("  $origen -> $n: $d min | Ruta: ${ruta.joinToString(" -> ")}")
        }
    }
}

fun menu() {
    while (true) {
        println("\n" + "=".repeat(55))
        println("SISTEMA DE RUTAS - VERSION ESTUDIANTES (KOTLIN)")
        println("=".repeat(55))
        println("1. Ruta más corta entre dos puntos")
        println("2. Ver todas las distancias desde un origen")
        println("3. Ver ubicaciones")
        println("4. Explicación breve de Dijkstra")
        println("5. Ver retos sugeridos")
        println("6. Salir")
        print("\nElige una opción (1-4): ")
        when (readLine()?.trim()) {
            "1" -> opcionRutaMasCorta()
            "2" -> opcionTodasLasDistancias()
            "3" -> mostrarUbicaciones()
            "4" -> explicarDijkstraBreve()
            "5" -> retos()
            "6" -> { println("\n¡Hasta luego! (Recuerda: cambia un peso y prueba otra vez.)"); return }
            else -> println("Opción inválida (intenta 1..6)")
        }
    }
}

// Lista de retos para practicar (los voy anotando mientras estudio)
fun retos() {
    println("\nRETOS SUGERIDOS (puedes editar el código y volver a correr):")
    println("1. Cambia el peso de A->C a 5. ¿Qué pasa con la ruta A->D?")
    println("2. Agrega un nodo H que vaya desde G con peso 4 y prueba A->H.")
    println("3. Elimina la arista D->E y observa B->E (¿sigue valiendo 27?).")
    println("4. Implementa una función que cuente cuántos tramos (saltos) tiene la ruta.")
    println("5. Añade una arista que cree un ciclo (por ejemplo G->A) y verifica que no se rompe.")
    println("6. Haz una versión que en lugar de minutos use 'costo' y otra que use 'distancia'.")
    println("7. Imprime también el 'padre' de cada nodo al final para ver el árbol de caminos mínimos.")
    println("8. Escribe tu propio código sin mirar este y compara.")
}

// ---------------------------------------------------------------------------
// 5. main() - Punto de entrada
// ---------------------------------------------------------------------------
fun main() {
    println("Ejemplo rápido (antes del menú): calcular ruta A -> D")
    val (dist, padres) = dijkstra(GRAFO, "A")
    val ruta = reconstruirRuta(padres, "A", "D")
    println("Ruta A->D: ${ruta?.joinToString(" -> ")} | Tiempo = ${dist["D"]}")
    println("(Puedes elegir la opción 4 del menú para repasar la explicación.)")

    menu()
}
