import { useState, useEffect } from 'react'
import useApi from '../../hooks/useApi'

function GroupList() {
  const [groups, setGroups] = useState([])
  const [loading, setLoading] = useState(true)
  const [isFormOpen, setIsFormOpen] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    currency: 'USD'
  })
  const [formError, setFormError] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [selectedGroup, setSelectedGroup] = useState(null)
  const { get, post } = useApi()

  useEffect(() => {
    const fetchGroups = async () => {
      try {
        setLoading(true)
        const response = await get('/api/v1/groups')
        setGroups(response.data || [])
      } catch (error) {
        console.error('Failed to fetch groups:', error)
        setGroups([])
      } finally {
        setLoading(false)
      }
    }

    fetchGroups()
  }, [get])

  const handleCreateClick = () => {
    setIsFormOpen(true)
    setFormError('')
  }

  const handleFormChange = (event) => {
    const { name, value } = event.target
    setFormData((current) => ({
      ...current,
      [name]: value
    }))
  }

  const handleCancel = () => {
    setIsFormOpen(false)
    setFormData({
      name: '',
      description: '',
      currency: 'USD'
    })
    setFormError('')
  }

  const handleSelectGroup = (group) => {
    setSelectedGroup((current) =>
      current?.id === group.id ? null : group
    )
  }

  const handleSubmit = async (event) => {
    event.preventDefault()

    if (!formData.name.trim()) {
      setFormError('Group name is required.')
      return
    }

    setSubmitting(true)
    setFormError('')

    try {
      const response = await post('/api/v1/groups', formData)
      const createdGroup = response.data
      setGroups((current) => [createdGroup, ...current])
      setIsFormOpen(false)
      setFormData({
        name: '',
        description: '',
        currency: 'USD'
      })
    } catch (error) {
      console.error('Failed to create group:', error)
      const message =
        error.response?.data?.detail ||
        error.response?.data?.message ||
        'Unable to create group. Please try again.'
      setFormError(message)
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) {
    return <div className="groups-container"><p>Loading groups...</p></div>
  }

  return (
    <div className="groups-container">
      <div className="groups-header">
        <h2>Groups</h2>
        <button className="btn btn-primary" onClick={handleCreateClick}>
          Create New Group
        </button>
      </div>

      {isFormOpen && (
        <form className="group-form" onSubmit={handleSubmit}>
          <div className="form-row">
            <label htmlFor="name">Name</label>
            <input
              id="name"
              name="name"
              type="text"
              value={formData.name}
              onChange={handleFormChange}
              placeholder="Group name"
              required
            />
          </div>

          <div className="form-row">
            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleFormChange}
              placeholder="Optional description"
            />
          </div>

          <div className="form-row">
            <label htmlFor="currency">Currency</label>
            <select
              id="currency"
              name="currency"
              value={formData.currency}
              onChange={handleFormChange}
            >
              <option value="USD">USD</option>
              <option value="EUR">EUR</option>
              <option value="GBP">GBP</option>
            </select>
          </div>

          {formError && <p className="form-error">{formError}</p>}

          <div className="form-actions">
            <button className="btn btn-secondary" type="button" onClick={handleCancel}>
              Cancel
            </button>
            <button className="btn btn-primary" type="submit" disabled={submitting}>
              {submitting ? 'Creating…' : 'Create Group'}
            </button>
          </div>
        </form>
      )}

      {groups.length === 0 ? (
        <div className="empty-state">
          <p>No groups yet. Create one to get started!</p>
        </div>
      ) : (
        <div className="groups-list">
          {groups.map((group) => (
            <div
              key={group.id}
              className={`group-card ${selectedGroup?.id === group.id ? 'selected' : ''}`}
              onClick={() => handleSelectGroup(group)}
            >
              <div className="group-card-details">
                <div>
                  <h3>{group.name}</h3>
                  {group.description && <p>{group.description}</p>}
                </div>
                <span className="group-currency">{group.currency}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {selectedGroup && (
        <div className="selected-group-panel">
          <div className="selected-group-header">
            <h3>Selected Group</h3>
            <button className="btn btn-secondary" type="button" onClick={() => setSelectedGroup(null)}>
              Clear selection
            </button>
          </div>
          <div className="selected-group-content">
            <h4>{selectedGroup.name}</h4>
            <p>{selectedGroup.description || 'No description provided.'}</p>
            <p>
              <strong>Currency:</strong> {selectedGroup.currency}
            </p>
          </div>
        </div>
      )}
    </div>
  )
}

export default GroupList
