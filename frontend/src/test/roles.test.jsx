import { describe, it, expect } from 'vitest'

function puedeEditarTarea(rol) {
  return rol === 'owner' || rol === 'editor'
}

function puedeEliminarProyecto(rol) {
  return rol === 'owner'
}

function puedeVerTareas(rol) {
  return rol === 'owner' || rol === 'editor' || rol === 'observer'
}

describe('Control de roles por proyecto', () => {
  it('el owner puede editar tareas', () => {
    expect(puedeEditarTarea('owner')).toBe(true)
  })

  it('el editor puede editar tareas', () => {
    expect(puedeEditarTarea('editor')).toBe(true)
  })

  it('el observer NO puede editar tareas', () => {
    expect(puedeEditarTarea('observer')).toBe(false)
  })

  it('solo el owner puede eliminar el proyecto', () => {
    expect(puedeEliminarProyecto('owner')).toBe(true)
    expect(puedeEliminarProyecto('editor')).toBe(false)
    expect(puedeEliminarProyecto('observer')).toBe(false)
  })

  it('todos los roles pueden ver las tareas', () => {
    expect(puedeVerTareas('owner')).toBe(true)
    expect(puedeVerTareas('editor')).toBe(true)
    expect(puedeVerTareas('observer')).toBe(true)
  })
})