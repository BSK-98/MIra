type props = {
    classText: string
}
const RecordIcon = ({ classText }: props) => {
    return <>
        <div className={"w-6 h-6 " + classText}>R</div>
    </>
}

export default RecordIcon