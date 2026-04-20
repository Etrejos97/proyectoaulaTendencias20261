import { describe, it, expect } from 'vitest'

// Simula la lógica de comentarios
function puedeEditarComentario(usuarioActual, autorComentario, esAdmin) {
  return esAdmin || usuarioActual === autorComentario
}

function puedeEliminarComentario(usuarioActual, autorComentario, esAdmin) {
  return esAdmin || usuarioActual === autorComentario
}

function validarComentario(texto) {
  return texto && texto.trim().length > 0
}

describe('Módulo de comentarios', () => {
  it('el autor puede editar su propio comentario', () => {
    expect(puedeEditarComentario('jdavid', 'jdavid', false)).toBe(true)
  })

  it('otro usuario NO puede editar un comentario ajeno', () => {
    expect(puedeEditarComentario('jdavid', 'admin', false)).toBe(false)
  })

  it('el admin puede editar cualquier comentario', () => {
    expect(puedeEditarComentario('admin', 'jdavid', true)).toBe(true)
  })

  it('el autor puede eliminar su propio comentario', () => {
    expect(puedeEliminarComentario('jdavid', 'jdavid', false)).toBe(true)
  })

  it('el admin puede eliminar cualquier comentario', () => {
    expect(puedeEliminarComentario('admin', 'jdavid', true)).toBe(true)
  })

  it('no se permite publicar comentarios vacíos', () => {
    expect(validarComentario('')).toBeFalsy()
    expect(validarComentario('   ')).toBeFalsy()
  })

  it('un comentario con texto válido pasa la validación', () => {
    expect(validarComentario('Buen trabajo')).toBeTruthy()
  })
})