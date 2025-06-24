@Test
public void testDeletePreApprovalPaymentsException() throws WVCPBusinessException {
    assertThrows(WVCPBusinessException.class, () -> {
        // Arrange
        DeletePaymentsRequest deletePaymetsRequest = new DeletePaymentsRequest();
        deletePaymetsRequest.setCompanyId("TEST123");
        deletePaymetsRequest.setTransactionIds(Stream.of(123456789L).collect(Collectors.toList()));

        User user = new User();
        user.setUserId("TEST123");

        UserInfo coreUserInfo = new UserInfo();
        coreUserInfo.setFullName("TestName");
        coreUserInfo.setEmailAddress("abc@wells.com");

        HttpSession httpSession = Mockito.mock(HttpSession.class);
        HttpServletRequest request = Mockito.mock(HttpServletRequest.class);
        HttpServletResponse response = Mockito.mock(HttpServletResponse.class);

        // 🟢 Stub ALL session attributes used in controller
        Mockito.when(httpSession.getAttribute(WebConstants.LOGGED_IN_USER)).thenReturn(user);
        Mockito.when(httpSession.getAttribute(SessionConstants.USER_ENTITLED_DIVISIONS_STR_LIST))
               .thenReturn(Arrays.asList("DIV1", "DIV2"));
        Mockito.when(httpSession.getAttribute(SessionConstants.USER_ENTITLED_ACCOUNTS))
               .thenReturn(new HashMap<>()); // or appropriate mock

        // 🟢 Mock session return from request
        Mockito.when(request.getSession(anyBoolean())).thenReturn(httpSession);

        // Act
        paymentsController.deletePreApprovalPayments(request, response, deletePaymetsRequest);
    });
}
