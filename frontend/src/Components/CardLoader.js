import React from 'react'
import { Card, Image, Loader } from 'semantic-ui-react'
import "./components.css"

const CardLoader = (props) => {
    return (
        <Card>
        <Card.Content className={"card-holder"}>
            <Loader active />
            <Image src={"https://react.semantic-ui.com/images/wireframe/short-paragraph.png"}/>
            <Image src={"https://react.semantic-ui.com/images/wireframe/short-paragraph.png"} className={"loader-image"} />
            <Image src={"https://react.semantic-ui.com/images/wireframe/short-paragraph.png"} className={"loader-image"} />
            <Image src={"https://react.semantic-ui.com/images/wireframe/short-paragraph.png"} className={"loader-image"} />
        </Card.Content>
        </Card>
    );
}

export default CardLoader