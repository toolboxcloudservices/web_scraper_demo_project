import React from 'react';
import {Button, Layout, Typography, Space, Card, Row, Col} from 'antd';
import {Link} from 'react-router-dom';
import {LaptopOutlined, GithubOutlined, IdcardOutlined} from '@ant-design/icons';

const {Paragraph} = Typography;
const {Content} = Layout;

function WelcomePage() {
    return (
        <Layout className="layout">
            <Content style={{padding: '50px', textAlign: 'center'}}>
                <div style={{maxWidth: '600px', margin: '0 auto'}}>
                    <Card title="👋 Welcome to the Web Scraper Demo!" bordered={false}>
                        <Paragraph>
                            This is a demo of my Web Scraping project that I built while I was working at
                            CyberTrustMass,
                            using <b>React</b> for the frontend and <b>Python Flask</b> for the backend.
                            The web scraper extracts valuable IT department contact information from town/city websites,
                            processes it,
                            and generates reports.
                        </Paragraph>
                        <Paragraph>
                            🚀 <b>Technologies Used:</b> React, Python Flask, Pandas, Ant Design, Excel Generation, Web
                            Scraping Libraries
                        </Paragraph>

                        <Space direction="vertical" size="large" style={{display: 'flex', justifyContent: 'center'}}>
                            <Link to="/scraper">
                                <Button
                                    type="primary"
                                    size="large"
                                    icon={<LaptopOutlined/>}
                                    style={{width: '200px', marginTop: '10px'}}
                                >
                                    Try the Web Scraper
                                </Button>
                            </Link>

                            <Paragraph>
                                Want to see your data results? Simply input the demo
                                URL <b>https://www.chatham-ma.gov</b> and hit 'Start Scraping'! The demo will guide you
                                through the entire process.
                            </Paragraph>

                            {/* Buttons in a Row */}
                            <Row gutter={16} justify="center" style={{marginTop: '20px'}}>
                                {/* GitHub Button with Icon */}
                                <Col>
                                    <a href="https://github.com/toolboxcloudservices" target="_blank"
                                       rel="noopener noreferrer">
                                        <Button
                                            type="default"
                                            size="large"
                                            icon={<GithubOutlined/>}
                                            style={{width: '200px'}}
                                        >
                                            View Code on GitHub
                                        </Button>
                                    </a>
                                </Col>

                                {/* Portfolio Button with Icon */}
                                <Col>
                                    <a href="https://deannasfolio.vercel.app/" target="_blank"
                                       rel="noopener noreferrer">
                                        <Button
                                            type="default"
                                            size="large"
                                            icon={<IdcardOutlined/>}
                                            style={{width: '200px'}}
                                        >
                                            View My Portfolio
                                        </Button>
                                    </a>
                                </Col>
                            </Row>
                        </Space>
                    </Card>
                </div>
            </Content>
        </Layout>
    );
}

export default WelcomePage;