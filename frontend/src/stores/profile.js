import { defineStore } from 'pinia'

export const useProfileStore = defineStore('profile', {
  state: () => ({
    avatar: localStorage.getItem('profile_avatar') || '', // base64 或文件URL
    nickname: localStorage.getItem('profile_nickname') || '',
    email: localStorage.getItem('profile_email') || '',
    bio: localStorage.getItem('profile_bio') || ''
  }),
  actions: {
    setAvatar(dataUrl) {
      this.avatar = dataUrl
      localStorage.setItem('profile_avatar', dataUrl)
    },
    setNickname(n) {
      this.nickname = n
      localStorage.setItem('profile_nickname', n)
    },
    setEmail(e) {
      this.email = e
      localStorage.setItem('profile_email', e)
    },
    setBio(b) {
      this.bio = b
      localStorage.setItem('profile_bio', b)
    }
  }
})