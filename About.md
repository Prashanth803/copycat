package com.wellsfargo.ps.service.sdd;

import com.wellsfargo.ps.bo.APDetailsDTO;
import com.wellsfargo.ps.bo.AddendumDTO;
import com.wellsfargo.ps.bo.NotifyRequestDetails;
import com.wellsfargo.ps.client.ws.C3GCommonClient;
import com.wellsfargo.ps.client.ws.RemittanceServiceClient;
import com.wellsfargo.ps.core.exception.PSException;
import com.wellsfargo.ps.dao.sdd.ISDDDao;
import com.wellsfargo.ps.dto.sharedservices.SDDNotifyRequest;
import com.wellsfargo.ps.dto.sharedservices.SDDNotifyResponse;
import com.wellsfargo.ps.util.APDetailDomUtil;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.core.io.FileSystemResource;

import java.io.File;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class SDDServiceImplTest {

    @Mock
    private ISDDDao sddDao;

    @Mock
    private RemittanceServiceClient remittanceServiceClient;

    @Mock
    private C3GCommonClient c3gCommonClient;

    @InjectMocks
    private SDDServiceImpl sddService;

    private APDetailsDTO detail;
    private NotifyRequestDetails notifyRequestDetails;
    private SDDNotifyRequest sddNotifyRequest;
    private LinkedHashMap<String, String> emailMap;

    @BeforeEach
    void setUp() {
        detail = new APDetailsDTO();
        detail.setTransactionId("T123");
        detail.setPayeeNotifiableFlag("Y");

        List<APDetailsDTO> detailList = new ArrayList<>();
        detailList.add(detail);

        notifyRequestDetails = new NotifyRequestDetails();
        notifyRequestDetails.setDetails(detailList);
        notifyRequestDetails.setRequestType("SDD");

        sddNotifyRequest = new SDDNotifyRequest();
        sddNotifyRequest.setApDetails(detailList);
        sddNotifyRequest.setRequestType("SDD");
        sddNotifyRequest.setEmailMap(new LinkedHashMap<>());

        emailMap = new LinkedHashMap<>();
    }

    @Test
    void testSendOneAtATimePublicMethod() throws Exception {
        ISDDDao mockDao = mock(ISDDDao.class);
        when(mockDao.isSDDRecordAlreadyExist(any(), any())).thenReturn(false);
        sddService.setSddDao(mockDao);

        // Since private method behavior can't be mocked, this will execute real logic
        assertThrows(PSException.class, () -> sddService.sendOneAtATime(sddNotifyRequest));
    }

    @Test
    void testGetOutputFileDirPrivate() throws Exception {
        Method method = SDDServiceImpl.class.getDeclaredMethod("getOutputFileDir");
        method.setAccessible(true);
        String path = (String) method.invoke(sddService);
        assertNotNull(path);
        assertTrue(path.contains("/log/"));
    }

    @Test
    void testDecryptPrivate() throws Exception {
        Method method = SDDServiceImpl.class.getDeclaredMethod("decrypt", String.class);
        method.setAccessible(true);

        assertThrows(Exception.class, () -> {
            method.invoke(sddService, "dummyEncrypted");
        });
    }

    @Test
    void testGetPackageIdPrivate() throws Exception {
        Method method = SDDServiceImpl.class.getDeclaredMethod("getPackageId", String.class);
        method.setAccessible(true);

        Long result = (Long) method.invoke(sddService, "12345");
        assertEquals(12345L, result);
    }

    @Test
    void testPaddKeyStatic() {
        String padded = SDDServiceImpl.paddKey("shortkey");
        assertEquals(16, padded.length());
    }

    @Test
    void testAsByteStatic() {
        byte[] bytes = SDDServiceImpl.asByte("4f4b");
        assertEquals(2, bytes.length);
    }

    @Test
    void testAsHexStatic() {
        byte[] input = new byte[]{0x4f, 0x4b};
        String hex = SDDServiceImpl.ashex(input);
        assertEquals("4f4b", hex);
    }
}
package com.wellsfargo.ps.service.sdd;

import com.wellsfargo.ps.bo.APDetailsDTO;
import com.wellsfargo.ps.bo.AddendumDTO;
import com.wellsfargo.ps.bo.NotifyRequestDetails;
import com.wellsfargo.ps.client.ws.C3GCommonClient;
import com.wellsfargo.ps.client.ws.RemittanceServiceClient;
import com.wellsfargo.ps.core.exception.PSException;
import com.wellsfargo.ps.dao.sdd.ISDDDao;
import com.wellsfargo.ps.dto.sharedservices.SDDNotifyRequest;
import com.wellsfargo.ps.dto.sharedservices.SDDNotifyResponse;
import com.wellsfargo.ps.util.APDetailDomUtil;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.core.io.FileSystemResource;

import java.io.File;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class SDDServiceImplTest {

    @Mock
    private ISDDDao sddDao;

    @Mock
    private RemittanceServiceClient remittanceServiceClient;

    @Mock
    private C3GCommonClient c3gCommonClient;

    @InjectMocks
    private SDDServiceImpl sddService;

    private APDetailsDTO detail;
    private NotifyRequestDetails notifyRequestDetails;
    private SDDNotifyRequest sddNotifyRequest;
    private LinkedHashMap<String, String> emailMap;

    @BeforeEach
    void setUp() {
        detail = new APDetailsDTO();
        detail.setTransactionId("T123");
        detail.setPayeeNotifiableFlag("Y");

        List<APDetailsDTO> detailList = new ArrayList<>();
        detailList.add(detail);

        notifyRequestDetails = new NotifyRequestDetails();
        notifyRequestDetails.setDetails(detailList);
        notifyRequestDetails.setRequestType("SDD");

        sddNotifyRequest = new SDDNotifyRequest();
        sddNotifyRequest.setApDetails(detailList);
        sddNotifyRequest.setRequestType("SDD");
        sddNotifyRequest.setEmailMap(new LinkedHashMap<>());

        emailMap = new LinkedHashMap<>();
    }

    @Test
    void testSendOneAtATimePublicMethod() throws Exception {
        ISDDDao mockDao = mock(ISDDDao.class);
        when(mockDao.isSDDRecordAlreadyExist(any(), any())).thenReturn(false);
        sddService.setSddDao(mockDao);

        // Since private method behavior can't be mocked, this will execute real logic
        assertThrows(PSException.class, () -> sddService.sendOneAtATime(sddNotifyRequest));
    }

    @Test
    void testGetOutputFileDirPrivate() throws Exception {
        Method method = SDDServiceImpl.class.getDeclaredMethod("getOutputFileDir");
        method.setAccessible(true);
        String path = (String) method.invoke(sddService);
        assertNotNull(path);
        assertTrue(path.contains("/log/"));
    }

    @Test
    void testDecryptPrivate() throws Exception {
        Method method = SDDServiceImpl.class.getDeclaredMethod("decrypt", String.class);
        method.setAccessible(true);

        assertThrows(Exception.class, () -> {
            method.invoke(sddService, "dummyEncrypted");
        });
    }

    @Test
    void testGetPackageIdPrivate() throws Exception {
        Method method = SDDServiceImpl.class.getDeclaredMethod("getPackageId", String.class);
        method.setAccessible(true);

        Long result = (Long) method.invoke(sddService, "12345");
        assertEquals(12345L, result);
    }

    @Test
    void testPaddKeyStatic() {
        String padded = SDDServiceImpl.paddKey("shortkey");
        assertEquals(16, padded.length());
    }

    @Test
    void testAsByteStatic() {
        byte[] bytes = SDDServiceImpl.asByte("4f4b");
        assertEquals(2, bytes.length);
    }

    @Test
    void testAsHexStatic() {
        byte[] input = new byte[]{0x4f, 0x4b};
        String hex = SDDServiceImpl.ashex(input);
        assertEquals("4f4b", hex);
    }
}
