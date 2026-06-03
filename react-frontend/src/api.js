const BASE = '/items'

export async function fetchItems(order = 'asc') {
  const res = await fetch(`${BASE}/?limit=100&order=${order}`)
  if (!res.ok) throw new Error('Failed to fetch items')
  return res.json()
}

export async function createItem(data) {
  const res = await fetch(`${BASE}/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  if (!res.ok) throw new Error('Failed to create item')
  return res.json()
}

export async function updateItem(id, data) {
  const res = await fetch(`${BASE}/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  if (!res.ok) throw new Error('Failed to update item')
  return res.json()
}

export async function deleteItem(id) {
  const res = await fetch(`${BASE}/${id}`, { method: 'DELETE' })
  if (!res.ok) throw new Error('Failed to delete item')
  return res.json()
}
