import React, { useState } from "react";
import { Layout, message, Spin, Alert, Card, Row, Col, Steps, Descriptions, Button } from "antd";
import Form from "./Form";
import Logs from "./Logs";
import Screenshots from "./Screenshots";
import { SearchOutlined } from '@ant-design/icons';


const { Header, Content } = Layout;
const { Step } = Steps;

const ScraperPage = () => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [screenshots, setScreenshots] = useState(null);
  const [loading, setLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState(0); // For tracking current step
  const [stepDescription, setStepDescription] = useState(""); // For tracking dynamic descriptions
  const [buttonLoading, setButtonLoading] = useState(false); // For button loading state
  const [reportUrl, setReportUrl] = useState(""); // To store the report URL

  // Message for error handling
  const handleError = (errorMsg) => {
      message.error(errorMsg);
      setError(errorMsg);
  };

  const handleStepChange = (newStep) => {
      setCurrentStep(newStep);
      // Update step descriptions based on the current step
      switch (newStep) {
          case 0:
              setStepDescription("Initializing the scraper...");
              break;
          case 1:
              setStepDescription("Scraping data from the website...");
              break;
          case 2:
              setStepDescription("Scraping complete. Data ready!");
              break;
          default:
              setStepDescription("");
      }
  };

  // Handle download of the report
  const handleDownload = () => {
      if (reportUrl) {
          window.location.href = reportUrl; // Trigger file download
      } else {
          message.error("Report URL not available.");
      }
  };

  // Make sure to set the report URL when data is received from the backend
  const handleBackendResponse = (response) => {
      setData(response.data); // Store the scraped data
      setScreenshots(response.screenshots); // Store screenshots
      setReportUrl(response.report_url); // Set the report URL from the backend
  };

  return (
      <Layout className="layout">
          <Header style={{color: "white", fontSize: "24px", fontWeight: "bold"}}>
             <SearchOutlined /> &nbsp; IT Department Web Scraper
          </Header>
          <Content style={{padding: "50px"}}>
              <Row gutter={16}>
                  <Col span={8}>
                      <Card title="Start Scraping" bordered={false}>
                          <Form
                              setData={setData}
                              setError={handleError}
                              setScreenshots={setScreenshots}
                              setLoading={setLoading}
                              setStep={handleStepChange}
                              buttonLoading={buttonLoading}
                              setButtonLoading={setButtonLoading}
                              setReportUrl={handleBackendResponse} // Pass handler for report URL
                          />

                          {/* Add Download Button if reportUrl is available */}
                          {reportUrl && (
                              <Button
                                  type="primary"
                                  onClick={handleDownload}
                                  style={{
                                      marginTop: "20px",
                                      display: "block",
                                      width: "200px",
                                      backgroundColor: "blue"
                                  }}
                              >
                                  Download XLS
                              </Button>
                          )}
                      </Card>

                      {/* New Process Logs Card */}
                      <Card title="Process Log" bordered={false} style={{marginTop: 20}}>
                          <Logs/> {/* Include the Logs component here */}
                      </Card>
                  </Col>

                  <Col span={16}>
                      {/* Display Progress Steps */}
                      <Steps current={currentStep} style={{marginBottom: 20}}>
                          <Step title="Starting" description={currentStep === 0 ? stepDescription : ""}/>
                          <Step title="In Progress" description={currentStep === 1 ? stepDescription : ""}/>
                          <Step title="Finished" description={currentStep === 2 ? stepDescription : ""}/>
                      </Steps>

                      {loading && (
                          <div style={{marginTop: 80, textAlign: "center"}}>
                              <Spin size="large"/>
                              <div style={{marginTop: 10, fontSize: "16px"}}>
                                  Data will display here one moment...
                              </div>
                          </div>
                      )}

                      {error && <Alert message={error} type="error" showIcon style={{marginTop: 20}}/>}

                      {data && (
                          <Card style={{marginTop: 20}}>
                              <Descriptions title="Scraping Results" bordered column={1}>
                                  {Object.entries(data).map(([key, value]) => (
                                      <Descriptions.Item key={key} label={key.replace(/_/g, " ")}>
                                          {typeof value === "object" ? JSON.stringify(value, null, 2) : value}
                                      </Descriptions.Item>
                                  ))}
                              </Descriptions>

                              {/* Add Download Button if reportUrl is available */}
                              {reportUrl && reportUrl.trim() !== "" && (
                                  <Button
                                      type="primary"
                                      onClick={handleDownload}
                                      style={{
                                          marginTop: "20px",
                                          display: "block",
                                          width: "200px",
                                          backgroundColor: "blue"
                                      }}
                                  >
                                      Download XLS
                                  </Button>
                              )}
                          </Card>
                      )}

                      {/* Screenshots Section */}
                      {screenshots && Object.keys(screenshots).length > 0 && (
                          <Card title="Screenshots" bordered={false} style={{marginTop: "20px"}}>
                              <Screenshots screenshots={screenshots}/>
                          </Card>
                      )}
                  </Col>
              </Row>
          </Content>
      </Layout>
  );
};

export default ScraperPage;
