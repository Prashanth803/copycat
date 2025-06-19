DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
DocumentBuilder builder = factory.newDocumentBuilder();
Document dummyDoc = builder.newDocument(); // Empty but valid DOM

when(apDomUtil.createApDetailRequest(any(), any(), any(), any(), any())).thenReturn(dummyDoc);
