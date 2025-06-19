import static org.mockito.Mockito.*;
import org.mockito.MockedStatic;
import org.junit.jupiter.api.Test;
import org.springframework.test.util.ReflectionTestUtils;

import java.io.File;
import java.io.FileWriter;
import java.util.*;

import com.wellsfargo.ps.dto.sharedservices.SDDNotifyRequest;
import com.wellsfargo.ps.dto.sharedservices.SDDNotifyResponse;
import com.wellsfargo.ps.bo.APDetailsDTO;
import com.wellsfargo.ps.bo.CardDTO;
import com.wellsfargo.ps.service.sdd.SDDServiceImpl;
import com.wellsfargo.ps.util.PDFGenerator;

class SDDServiceImplTest {

    @Test
    void testSendOneAtATime_withMockedPDFGenerator() throws Exception {
        // Arrange
        SDDServiceImpl sddService = new SDDServiceImpl();

        // Set up required fields using ReflectionTestUtils
        String outputDir = System.getProperty("java.io.tmpdir");
        ReflectionTestUtils.setField(sddService, "sddOutputFileDir", outputDir);

        File xslFile = new File(outputDir, "dummy.xsl");
        try (FileWriter writer = new FileWriter(xslFile)) {
            writer.write("""
                <xsl:stylesheet version="1.0"
                    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
                    <xsl:template match="/">
                        <html><body><h2>Test PDF</h2></body></html>
                    </xsl:template>
                </xsl:stylesheet>
            """);
        }
        ReflectionTestUtils.setField(sddService, "sddXslFile", xslFile.getAbsolutePath());

        // Prepare dummy DTOs
        APDetailsDTO detail = new APDetailsDTO();
        detail.setTransactionId("TX123");
        detail.setPayeeNotifiableFlag("Y");

        CardDTO card = mock(CardDTO.class);
        when(card.getPan()).thenReturn("1234567890123456");
        detail.setCpn(card);

        List<APDetailsDTO> details = List.of(detail);

        SDDNotifyRequest request = new SDDNotifyRequest();
        request.setApDetails(details);
        request.setRequestType("SDD");
        request.setEmailMap(new LinkedHashMap<>());

        // 🧩 Mock static PDFGenerator method
        try (MockedStatic<PDFGenerator> pdfMock = mockStatic(PDFGenerator.class)) {
            pdfMock.when(() -> PDFGenerator.convertDom2PDF(any(), any(), any()))
                   .thenAnswer(invocation -> null); // ✅ Do nothing

            // Act
            SDDNotifyResponse response = sddService.sendOneAtATime(request);

            // Assert
            assertNotNull(response);
            assertEquals("SDD", response.getRequestType());

            // Optional verify
            pdfMock.verify(() -> PDFGenerator.convertDom2PDF(any(), any(), any()), atLeastOnce());
        }
    }
}
