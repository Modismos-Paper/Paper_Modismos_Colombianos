/**
 * GENERADOR DE DATASET JSON - DICCIONARIO DE COLOMBIANISMOS
 * 
 * Extrae todas las entradas del diccionario DICOL via API,
 * normaliza definiciones/ejemplos anidados, y genera archivo JSON unificado.
 */

import DictionaryRepository from './DictionaryRepository.js';
import * as fs from 'fs';

// ========================================================================
// CONFIGURACIÓN
// ========================================================================

const ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÑ'.split('');
const DICTIONARY_ID = "642af684da699a2968ef1d19";

// ========================================================================
// EXTRACCIÓN Y NORMALIZACIÓN DE ACEPCIONES
// ========================================================================

function primeraAcepcionExtract(acepcion){
    let definicion = 'Definición no encontrada.';
    let ejemplo = 'Ejemplo no encontrado.';

    if (!acepcion) {
        return { definicion, ejemplo };
    }

    // Maneja múltiples formatos: string, objeto con 'texto', anidamiento, o array
    if (acepcion.definicion) {
        let defData = acepcion.definicion;

        if (typeof defData === 'string') {
            definicion = defData;
        } else if (defData.texto) {
            definicion = defData.texto;
        } else if (defData.definicion) {
            // A veces la definición está anidada: { definicion: { definicion: "texto" } }
            if (typeof defData.definicion === 'string') {
                definicion = defData.definicion;
            } else if (defData.definicion.definicion) {
                definicion = defData.definicion.definicion;
            }
        } else if (Array.isArray(defData) && defData.length > 0 && defData[0].texto) {
            definicion = defData[0].texto;
        }
    }

    // Maneja ejemplos con estructura similar a definiciones
    if (acepcion.ejemplo) {
        let ejData = acepcion.ejemplo;

        if (typeof ejData === 'string') {
            ejemplo = ejData;
        } else if (ejData.ejemplo) {
            // Puede ser un objeto { ejemplo: "texto" } o un array [{ ejemplo: "texto" }]
            if (typeof ejData.ejemplo === 'string') {
                ejemplo = ejData.ejemplo;
            } else if (Array.isArray(ejData.ejemplo) && ejData.ejemplo.length > 0) {
                ejemplo = ejData.ejemplo[0];
            }
        } else if (Array.isArray(ejData) && ejData.length > 0) {
            // Puede ser un array de strings o de objetos
            if (typeof ejData[0] === 'string') {
                ejemplo = ejData[0];
            } else if (ejData[0].ejemplo) {
                ejemplo = ejData[0].ejemplo;
            }
        }
    }

    return { definicion, ejemplo };
}

// ========================================================================
// FUNCIONES DE GUARDADO JSON
// ========================================================================

function saveEntryAsJson(entry) {
    // Guarda entrada individual con nombre de archivo sanitizado
    if (!entry || !entry.lemmaSign) {
        console.error("No se puede guardar el entry: objeto inválido.");
        return;
    }
    // Crea un nombre de archivo seguro a partir del lema
    const safeLemma = entry.lemmaSign.replace(/[^a-z0-9]/gi, '_').toLowerCase();
    const filename = `entry_${safeLemma}.json`;
    try {
        // Convierte el objeto a un string JSON formateado
        const jsonContent = JSON.stringify(entry, null, 2);
        fs.writeFileSync(filename, jsonContent, 'utf8');
        console.log(`Entry para '${entry.lemmaSign}' guardado en ${filename}`);
    } catch (err) {
        console.error(`Error al guardar el JSON del entry '${entry.lemmaSign}':`, err);
    }
}

// ========================================================================
// EXTRACCIÓN DE DATOS DE ENTRADAS
// ========================================================================

function extractEntryData(entry) {
    if (!entry || !entry.lemmaSign) {
        return []; 
    }

    const lema = entry.lemmaSign;
    const results = [];

    // Caso 1: Array de acepciones → genera una fila por cada definición
    if (Array.isArray(entry.acepcion)) {
        for (const acepcion of entry.acepcion) {
            const { definicion, ejemplo } = primeraAcepcionExtract(acepcion);
            results.push({
                palabra: lema,
                significado: definicion.trim(),
                ejemplo: ejemplo.trim(),
                región: ""
            });
        }
        return results;
    }

    // Caso 2: Array de SubEntradas → extrae primera acepción de cada una
    if (Array.isArray(entry.SubEntrada)) {
        for (const sub of entry.SubEntrada) {
            if (sub.acepcion) {
                // Tomamos la primera acepción de esta SubEntrada.
                const acepcion = Array.isArray(sub.acepcion) ? sub.acepcion[0] : sub.acepcion;
                const { definicion, ejemplo } = primeraAcepcionExtract(acepcion);
                results.push({
                    palabra: lema,
                    significado: definicion.trim(),
                    ejemplo: ejemplo.trim(),
                    región: ""
                });
            }
        }
        return results;
    }

    // Caso 3: Acepción única (sin arrays)
    let primeraAcepcion = null;

    if (entry.acepcion) {
        primeraAcepcion = entry.acepcion;
    } else if (entry.SubEntrada && entry.SubEntrada.acepcion) { // 'SubEntrada' es un objeto único.
        primeraAcepcion = Array.isArray(entry.SubEntrada.acepcion) ? entry.SubEntrada.acepcion[0] : entry.SubEntrada.acepcion;
    }

    if (!primeraAcepcion) {
        return results;
    }

    const { definicion, ejemplo } = primeraAcepcionExtract(primeraAcepcion);
    
    results.push({
        palabra: lema,
        significado: definicion.trim(),
        ejemplo: ejemplo.trim(),
        región: ""
    });

    return results;
}

function saveAllEntriesAsJson(entries, filename) {
    // Serializa y guarda array completo de entradas en un solo archivo JSON
    try {
        const jsonContent = JSON.stringify(entries, null, 2);
        fs.writeFileSync(filename, jsonContent, 'utf8');
        console.log(`\nTodas las entradas guardadas con éxito en '${filename}'.`);
    } catch (err) {
        console.error("Error al guardar el archivo JSON completo:", err);
    }
}

// ========================================================================
// PIPELINE PRINCIPAL
// ========================================================================

async function init() {
    const repo = new DictionaryRepository();
    let allEntries = [];

    console.log("Iniciando carga y acumulación de datos...");
    
    // Itera por cada letra del alfabeto español
    for (const letter of ALPHABET) {
        console.log(`Cargando entradas con: ${letter}`);

        try {
            const entries = await repo.fetchDictionaryEntries(DICTIONARY_ID, letter, 'api');
            
            if (entries.length === 0) {
                console.log(`No se encontraron entradas para la letra ${letter}.`);
                continue;
            }

            // Extrae y acumula datos normalizados de cada entrada
            entries.forEach(entry => {
                const extractedData = extractEntryData(entry);
                allEntries.push(...extractedData);
            });
            
        } catch (error) {
            console.error(`Error al cargar entradas para la letra ${letter}:`, error.message || error);
        }
    }
    
    // Guarda dataset completo en archivo JSON unificado
    const jsonFilename = "../DICOL.json";
    saveAllEntriesAsJson(allEntries, jsonFilename);
    
    console.log("\nProceso de extracción de diccionario completado.");
}

init();