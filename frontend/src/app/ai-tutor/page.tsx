'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Card } from '@/components/ui/Card'
import { aiApi } from '@/lib/api'
import { Message } from '@/types'
import { Send, Brain } from 'lucide-react'

export default function AITutorPage() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [conversationId, setConversationId] = useState<number | null>(null)

  const startConversation = async () => {
    try {
      const response = await aiApi.startConversation({})
      setConversationId(response.data.id)
    } catch (error) {
      console.error('Failed to start conversation:', error)
    }
  }

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    if (!conversationId) {
      await startConversation()
      return
    }

    const userMessage: Message = {
      id: Date.now(),
      conversation: conversationId,
      role: 'user',
      content: input,
      created_at: new Date().toISOString(),
    }

    setMessages([...messages, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await aiApi.ask(conversationId.toString(), input)
      setMessages([...messages, userMessage, response.data.answer])
    } catch (error) {
      console.error('Failed to send message:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-6">
          <h1 className="text-3xl font-bold mb-2">AI 튜터</h1>
          <p className="text-muted-foreground">
            Claude AI와 1:1 대화하며 궁금한 것을 물어보세요
          </p>
        </div>

        <Card className="h-[600px] flex flex-col">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.length === 0 ? (
              <div className="text-center py-16">
                <Brain className="w-16 h-16 mx-auto mb-4 text-primary opacity-50" />
                <h3 className="text-lg font-semibold mb-2">AI 튜터에게 물어보세요</h3>
                <p className="text-muted-foreground">
                  학습 중 궁금한 것이 있으면 언제든지 질문하세요
                </p>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${
                    message.role === 'user' ? 'justify-end' : 'justify-start'
                  }`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg p-4 ${
                      message.role === 'user'
                        ? 'bg-primary text-primary-foreground'
                        : 'bg-gray-100'
                    }`}
                  >
                    <p className="whitespace-pre-wrap">{message.content}</p>
                  </div>
                </div>
              ))
            )}
            {loading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 rounded-lg p-4">
                  <div className="flex gap-2">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100" />
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200" />
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Input */}
          <form onSubmit={sendMessage} className="p-4 border-t">
            <div className="flex gap-2">
              <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="질문을 입력하세요..."
                disabled={loading}
              />
              <Button type="submit" disabled={loading}>
                <Send className="w-4 h-4" />
              </Button>
            </div>
          </form>
        </Card>
      </div>
    </div>
  )
}
