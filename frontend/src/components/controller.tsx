import { useState } from "react"
import Title from "./Title"
import RecorderMessage from "./RecorderMessage"
import axios from "axios"

const Controller = () => {
    const [isLoading, setIsLoading] = useState (false)
    const [messages, setMessages] = useState<any[]> ([])

    const createBlobUrl = (data: any) => {
        const blob = new Blob ([data], {type: "audio/mpeg"})
        const url = window.URL.createObjectURL (blob);
        return url
    }

    const handleStop = async (blobUrl: string) => {
        setIsLoading (true)
        const myMsg = {
            sender: "me",
            blobUrl
        }
        const msgsArr = [ ...messages, myMsg ]

        fetch (blobUrl).then ((res) => res.blob()).then( async (blob) => {
            const formData = new FormData ()
            formData.append("file", blob, "myfile.wav")

            await axios.post ("https://mira-owtz.onrender.com/post-audio", formData, {
                headers: {
                    "Content-Type": "audio/mpeg"
                },
                responseType: "arraybuffer"
            }).then ((res: any) =>{
                const blob = res.data
                const audio = new Audio

                audio.src = createBlobUrl (blob)
                const MiraMsg = {sender: "Mira", blobUrl: audio.src}
                msgsArr.push (MiraMsg)
                setMessages (msgsArr)
            }).catch ((err) => {
                console.error (err.message)
                setIsLoading (false)
            })
        })

        setIsLoading (false)
    }

    return <div className="h-screen overflow-y-hidden">
        <Title setMessages={ setMessages } />
        <div className="flex flex-col justify-between h-full overflow-y-scroll pb-96">
            {/* conversation */}
            <div className="mt-5 px-5">
                {messages?.map ((audio, index) => {
                    return <div key={index + audio.sender} className={"flex flex-col " + (audio.sender == "Mira" && "flex items-end")}>
                        {/* sender */}
                        <div className="mt-4">
                            <p className={audio.sender == "Mira" ? "text-right mr-2 italic text-pink-500": "mt-2 italic text-blue-500"}>
                                {audio.sender}
                            </p>
                            {/* audio message */}
                            <audio src={audio.blobUrl} className="appearance-none" controls autoPlay />
                        </div>
                    </div>
                })}

                {messages.length == 0 && !isLoading && (
                    <div className="text-blue-500 italic font-light mt-10 animate-pulse">Send Mire A Message</div>
                )}

                {isLoading && (
                    <div className="text-blue-500 italic font-light mt-10 animate-pulse">Give Me a moment</div>
                )}
            </div>

            <div className="fixed bottom-0 w-full py-6 border-t text-center bg-gradient-to-r from-slate-500 to-slate-700">
                <div className="flex justify-center items-center w-full">
                    <RecorderMessage handleStop={handleStop} />
                </div>
            </div>
            {/* Recorder */}
        </div>
    </div>
}

export default Controller