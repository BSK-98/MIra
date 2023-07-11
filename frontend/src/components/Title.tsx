import axios from "axios"
import { useState } from "react"

type props = {
    setMessages: any
}

const Title = ({ setMessages}: props) => {
    const [isResetting, setIsResetting] = useState (false)
    const resetConversion = async () => {
        setIsResetting (true)

        await axios.get ("http://localhost:8000/reset-chats").then ((res) => {
            if (res.status == 200) {
                alert (res.data)
                setMessages ([])
            }else {
                console.error ("there was an error with the API Request")
            }
        }).catch ((err) => {
            console.error (err.message)
        })

        setIsResetting (false)
    }


    return <div className="flex justify-between w-full items-center p-4 bg-slate-700 text-white font-bold shadow">
        <div className="italic">Mira</div>
        <button onClick={resetConversion} className={"transition-all duration-300 text-blue-300 hover:text-pink-500 " + (isResetting && "animate-pulse")}>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                <path strokeLinecap="round" strokeLinejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
            </svg>


        </button>
    </div>
}

export default Title