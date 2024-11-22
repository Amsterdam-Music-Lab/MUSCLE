/**
 *
 * @param  {...string} classes
 * @returns string
 */
export function classNames(...classes: (string | undefined | null | false)[]): string {
    return classes.filter(Boolean).join(' ')
}

export default classNames
