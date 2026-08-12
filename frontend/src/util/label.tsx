export const renderLabel = (label: string, size = "fa-lg") => {
    if (!label) return label
    if (label.startsWith('http')) return <img src={label}/>
    else return label
}
