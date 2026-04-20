import { describe, it, expect } from 'vitest'

function agregarEtiqueta(etiquetas, nueva) {
  if (!nueva || etiquetas.includes(nueva)) return etiquetas
  return [...etiquetas, nueva]
}

function eliminarEtiqueta(etiquetas, nombre) {
  return etiquetas.filter(e => e !== nombre)
}

describe('Gestión de etiquetas (tags)', () => {
  it('agrega una etiqueta nueva correctamente', () => {
    const resultado = agregarEtiqueta([], 'urgente')
    expect(resultado).toContain('urgente')
  })

  it('no agrega etiquetas duplicadas', () => {
    const resultado = agregarEtiqueta(['urgente'], 'urgente')
    expect(resultado).toHaveLength(1)
  })

  it('una tarea puede tener múltiples etiquetas', () => {
    let tags = []
    tags = agregarEtiqueta(tags, 'urgente')
    tags = agregarEtiqueta(tags, 'bug')
    tags = agregarEtiqueta(tags, 'frontend')
    expect(tags).toHaveLength(3)
  })

  it('no agrega etiquetas vacías', () => {
    const resultado = agregarEtiqueta(['urgente'], '')
    expect(resultado).toHaveLength(1)
  })

  it('elimina una etiqueta correctamente', () => {
    const resultado = eliminarEtiqueta(['urgente', 'bug'], 'urgente')
    expect(resultado).not.toContain('urgente')
    expect(resultado).toContain('bug')
  })
})