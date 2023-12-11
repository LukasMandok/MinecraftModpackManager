import dayjs from 'dayjs'
// import { useTags } from './stores/tags'

export default {
    install(app) {
        app.config.globalProperties.$dayjs = dayjs

        app.config.globalProperties.$capitalizeString = capitalizeString
        app.config.globalProperties.$formatNumber = formatNumber
        app.config.globalProperties.$formatCategory = formatCategory
        app.config.globalProperties.$formatProjectType = formatProjectType
        app.config.globalProperties.$formatCategoryHeader = formatCategoryHeader
        app.config.globalProperties.$formatVersions = formatVersions
        app.config.globalProperties.$external = external
    }
}

export const capitalizeString = (name) => {
    return name ? name.charAt(0).toUpperCase() + name.slice(1) : name
}

export const formatNumber = (number) => {
    return new Intl.NumberFormat().format(number)
}

export const formatProjectType = (name) => {
    if (name === 'resourcepack') {
        return 'Resource Pack'
    } else if (name === 'datapack') {
        return 'Data Pack'
    }

    return capitalizeString(name)
}

export const formatCategory = (name) => {
    if (name === 'neoforge') {
        return 'NeoForge'
    } else if (name === 'worldgen') {
        return 'World Generation'
    } else if (name === 'datapack') {
        return 'Data Pack'
    }
}

export const formatCategoryHeader = (name) => {
    return capitalizeString(name)
}

export const formatVersions = (versionArray) => {
    const tag = useTags()
    const allVersions = tag.value.gameVersions.slice().reverse()
    const allReleases = allVersions.filter((x) => x.version_type === 'release')

    const intervals = []
    let currentInterval = 0

    // This function creates intervals of versions based on their distance from the previous version.
    for (let i = 0; i < versionArray.length; i++) {
        const index = allVersions.findIndex((x) => x.version === versionArray[i])
        const releaseIndex = allReleases.findIndex((x) => x.version === versionArray[i])

        if (i === 0) {
            intervals.push([[versionArray[i], index, releaseIndex]])
        } else {
            const intervalBase = intervals[currentInterval]

            if (
                (index - intervalBase[intervalBase.length - 1][1] === 1 ||
                    releaseIndex - intervalBase[intervalBase.length - 1][2] === 1) &&
                (allVersions[intervalBase[0][1]].version_type === 'release' ||
                    allVersions[index].version_type !== 'release')
            ) {
                intervalBase[1] = [versionArray[i], index, releaseIndex]
            } else {
                currentInterval += 1
                intervals[currentInterval] = [[versionArray[i], index, releaseIndex]]
            }
        }
    }

    // This function takes in an array of intervals and returns a new array of intervals with all snapshots replaced with the release version that they were released from.
    const newIntervals = []
    for (let i = 0; i < intervals.length; i++) {
        const interval = intervals[i]

        if (interval.length === 2 && interval[0][2] !== -1 && interval[1][2] === -1) {
            let lastSnapshot = null
            for (let j = interval[1][1]; j > interval[0][1]; j--) {
                if (allVersions[j].version_type === 'release') {
                    newIntervals.push([
                        interval[0],
                        [
                            allVersions[j].version,
                            j,
                            allReleases.findIndex((x) => x.version === allVersions[j].version),
                        ],
                    ])

                    if (lastSnapshot !== null && lastSnapshot !== j + 1) {
                        newIntervals.push([[allVersions[lastSnapshot].version, lastSnapshot, -1], interval[1]])
                    } else {
                        newIntervals.push([interval[1]])
                    }

                    break
                } else {
                    lastSnapshot = j
                }
            }
        } else {
            newIntervals.push(interval)
        }
    }

    const output = []

    for (const interval of newIntervals) {
        if (interval.length === 2) {
            output.push(`${interval[0][0]}–${interval[1][0]}`)
        } else {
            output.push(interval[0][0])
        }
    }

    return (output.length === 0 ? versionArray : output).join(', ')
}

export const external = () => {
    // console.log("Called external function")
    const cosmetics = useCosmetics()
    // console.log("cosmetics: ", cosmetics)
    // console.log("external: ", cosmetics.externalLinksNewTab  ? '_blank' : '')
    return cosmetics.externalLinksNewTab ? '_blank' : ''
}
