export const renderLabel = (label: string) => {
    if (!label) return label
    if (label.startsWith('<')) {
        return (
            <div class="label-image" dangerouslySetInnerHTML={{ __html: label }}/>
        )
    }
    else return label
}
