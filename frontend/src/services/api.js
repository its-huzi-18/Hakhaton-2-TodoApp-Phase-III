// frontend/src/services/api.js
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';

class ApiService {
  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  // Helper function to get the token from localStorage
  getAuthToken() {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('token');
    }
    return null;
  }

  async sendMessage(userId, message, conversationId = null) {
    try {
      // Endpoint: POST /api/{user_id}/chat
      const endpoint = `${this.baseUrl}/${userId}/chat`;

      const token = this.getAuthToken();

      const headers = {
        'Content-Type': 'application/json',
      };

      // Add authorization header if token exists
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({
          content: message
        })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(`HTTP error! status: ${response.status} - ${errorData.detail || 'Unknown error'}`);
      }

      const data = await response.json();

      // Return the response in a format compatible with the frontend
      return {
        response: data.content || data.response,
        conversation_id: data.conversation_id,
        tool_calls: data.tool_calls || [],
        task_updates: data.task_updates || []
      };
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }

  async getConversations(userId) {
    try {
      const endpoint = `${this.baseUrl}/conversations/${userId}`;
      const token = this.getAuthToken();

      const headers = {
        'Content-Type': 'application/json',
      };

      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(endpoint, {
        method: 'GET',
        headers: headers
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error getting conversations:', error);
      throw error;
    }
  }

  async deleteConversation(conversationId) {
    try {
      const endpoint = `${this.baseUrl}/conversations/${conversationId}`;
      const token = this.getAuthToken();

      const headers = {};

      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(endpoint, {
        method: 'DELETE',
        headers: headers
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return true;
    } catch (error) {
      console.error('Error deleting conversation:', error);
      throw error;
    }
  }
}

export default new ApiService();
