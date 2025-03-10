import Disqus from "disqus-react"
import { baseUrl, disqusShortname } from "../reducers/store"

export const CustomDisqus = ({ id, title }) => {

    return (
        <Disqus.DiscussionEmbed
            shortname={disqusShortname}
            config={{
                url: baseUrl,
                identifier: id,
                title: title
            }}
        />
    )
}