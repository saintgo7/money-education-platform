'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { certificatesApi } from '@/lib/api'
import { Certificate } from '@/types'
import { Award, Download, Share2, Calendar } from 'lucide-react'
import { formatDate } from '@/lib/utils'

export default function CertificatesPage() {
  const [certificates, setCertificates] = useState<Certificate[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchCertificates()
  }, [])

  const fetchCertificates = async () => {
    try {
      const response = await certificatesApi.getMyCertificates()
      setCertificates(response.data)
    } catch (error) {
      console.error('Failed to fetch certificates:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleDownload = async (certificateId: number) => {
    try {
      const response = await certificatesApi.downloadCertificate(certificateId.toString())
      const blob = new Blob([response.data], { type: 'application/pdf' })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `certificate-${certificateId}.pdf`
      link.click()
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Failed to download certificate:', error)
      alert('인증서 다운로드에 실패했습니다.')
    }
  }

  const handleShare = (certificate: Certificate) => {
    const shareUrl = `${window.location.origin}/certificates/${certificate.certificate_id}`
    navigator.clipboard.writeText(shareUrl)
    alert('인증서 링크가 복사되었습니다!')
  }

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="animate-pulse space-y-4">
            <div className="h-8 bg-gray-200 rounded w-1/3" />
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="h-64 bg-gray-200 rounded-lg" />
              ))}
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">내 수료증</h1>
          <p className="text-muted-foreground">
            완료한 코스의 수료증을 확인하고 다운로드하세요
          </p>
        </div>

        {certificates.length === 0 ? (
          <Card>
            <CardContent className="p-16 text-center">
              <Award className="w-16 h-16 mx-auto mb-4 text-gray-300" />
              <h3 className="text-lg font-semibold mb-2">
                아직 수료증이 없습니다
              </h3>
              <p className="text-muted-foreground mb-6">
                코스를 완료하고 수료증을 받아보세요
              </p>
              <Button onClick={() => (window.location.href = '/courses')}>
                코스 둘러보기
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {certificates.map((certificate) => (
              <Card key={certificate.id} className="overflow-hidden">
                <div className="bg-gradient-to-br from-blue-500 to-purple-600 p-8 text-white">
                  <Award className="w-16 h-16 mb-4 opacity-80" />
                  <h3 className="text-xl font-bold mb-2">수료증</h3>
                  <p className="text-sm opacity-90">
                    Certificate ID: {certificate.certificate_id}
                  </p>
                </div>
                <CardContent className="p-6">
                  <h4 className="font-semibold text-lg mb-2">
                    {certificate.course_title}
                  </h4>
                  <p className="text-sm text-muted-foreground mb-4">
                    {certificate.student_name}
                  </p>

                  <div className="flex items-center gap-2 text-sm text-muted-foreground mb-6">
                    <Calendar className="w-4 h-4" />
                    <span>발급일: {formatDate(certificate.issued_at)}</span>
                  </div>

                  <div className="flex gap-2">
                    <Button
                      onClick={() => handleDownload(certificate.id)}
                      className="flex-1"
                    >
                      <Download className="w-4 h-4 mr-2" />
                      다운로드
                    </Button>
                    <Button
                      variant="outline"
                      onClick={() => handleShare(certificate)}
                    >
                      <Share2 className="w-4 h-4 mr-2" />
                      공유
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
