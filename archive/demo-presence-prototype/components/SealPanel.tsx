type Props = {
  confidence: number
  conflict: number
  sealState: string
}

export default function SealPanel({ confidence, conflict, sealState }: Props) {
  return (
    <div className="border rounded-xl p-4">
      <p>Confidence: {confidence}</p>
      <p>Conflict: {conflict}</p>
      <p>Seal: {sealState}</p>
    </div>
  )
}
