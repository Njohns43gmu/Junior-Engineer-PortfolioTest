import { useState, useEffect, useCallback } from 'react'
import { fetchItems, createItem, updateItem, deleteItem } from './api'

function App() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // New item form state
  const [newTitle, setNewTitle] = useState('')
  const [newDesc, setNewDesc] = useState('')
  const [creating, setCreating] = useState(false)

  // Inline edit state: { id, title, description }
  const [editing, setEditing] = useState(null)
  const [saving, setSaving] = useState(false)
  const [order, setOrder] = useState('asc')

  const load = useCallback(async (ord = order) => {
    try {
      setError(null)
      const data = await fetchItems(ord)
      setItems(data)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { load(order) }, [load, order])

  function toggleOrder() {
    const next = order === 'asc' ? 'desc' : 'asc'
    setOrder(next)
  }

  async function handleCreate(e) {
    e.preventDefault()
    if (!newTitle.trim()) return
    setCreating(true)
    try {
      await createItem({ title: newTitle.trim(), description: newDesc.trim() })
      setNewTitle('')
      setNewDesc('')
      await load()
    } catch (e) {
      setError(e.message)
    } finally {
      setCreating(false)
    }
  }

  async function handleSave(id) {
    setSaving(true)
    try {
      await updateItem(id, { title: editing.title, description: editing.description })
      setEditing(null)
      await load()
    } catch (e) {
      setError(e.message)
    } finally {
      setSaving(false)
    }
  }

  async function handleDelete(id) {
    if (!window.confirm('Delete this item?')) return
    try {
      await deleteItem(id)
      await load()
    } catch (e) {
      setError(e.message)
    }
  }

  return (
    <>
      <h1>Items Manager</h1>

      {/* Create form */}
      <div className="card">
        <h2>Add New Item</h2>
        <form onSubmit={handleCreate}>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="title">Title</label>
              <input
                id="title"
                type="text"
                placeholder="Item title"
                value={newTitle}
                onChange={e => setNewTitle(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="desc">Description</label>
              <input
                id="desc"
                type="text"
                placeholder="Item description"
                value={newDesc}
                onChange={e => setNewDesc(e.target.value)}
              />
            </div>
            <button type="submit" className="btn-primary" disabled={creating}>
              {creating ? 'Adding…' : 'Add Item'}
            </button>
          </div>
        </form>
        {error && <p className="error">{error}</p>}
      </div>

      {/* Items table */}
      <div className="card">
        <h2>All Items</h2>
        {loading ? (
          <p className="empty">Loading…</p>
        ) : items.length === 0 ? (
          <p className="empty">No items yet. Add one above.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th style={{ width: 70, cursor: 'pointer', userSelect: 'none' }} onClick={toggleOrder}>
                  ID {order === 'asc' ? '▲' : '▼'}
                </th>
                <th>Title</th>
                <th>Description</th>
                <th style={{ width: 150 }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {items.map(item => (
                <tr key={item.id}>
                  <td>{item.id}</td>
                  <td>
                    {editing?.id === item.id ? (
                      <input
                        type="text"
                        value={editing.title}
                        onChange={e => setEditing(ed => ({ ...ed, title: e.target.value }))}
                      />
                    ) : item.title}
                  </td>
                  <td>
                    {editing?.id === item.id ? (
                      <input
                        type="text"
                        value={editing.description}
                        onChange={e => setEditing(ed => ({ ...ed, description: e.target.value }))}
                      />
                    ) : item.description}
                  </td>
                  <td>
                    <div className="actions">
                      {editing?.id === item.id ? (
                        <>
                          <button className="btn-success" onClick={() => handleSave(item.id)} disabled={saving}>
                            {saving ? '…' : 'Save'}
                          </button>
                          <button className="btn-ghost" onClick={() => setEditing(null)}>Cancel</button>
                        </>
                      ) : (
                        <>
                          <button className="btn-primary" onClick={() => setEditing({ id: item.id, title: item.title, description: item.description })}>
                            Edit
                          </button>
                          <button className="btn-danger" onClick={() => handleDelete(item.id)}>
                            Delete
                          </button>
                        </>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </>
  )
}

export default App
