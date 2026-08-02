import apiClient from '@/api/client';
import { API_ENDPOINTS } from '@/constants/api';

export const uploadApi = {
  uploadFile: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return apiClient
      .post('/uploads', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      .then((r) => r.data);
  },
};
