from plenum.common.signer_simple import SimpleSigner
from sovrin_client.agent.constants import EVENT_NOTIFY_MSG
from sovrin_client.client.wallet.wallet import Wallet
from stp_core.common.log import getlogger
from sovrin_client.agent.runnable_agent import RunnableAgent
from sovrin_client.agent.agent import create_client

from sovrin_client.agent.walleted_agent import WalletedAgent
from sovrin_client.test.agent.helper import buildThriftWallet
from sovrin_client.test.client.TestClient import TestClient

logger = getlogger()

THRIFT_SEED = b'Thrift00000000000000000000000000'


class ThriftAgent(WalletedAgent):

    async def postProofVerif(self, claimName, link, frm):
        if claimName == "Loan-Application-Basic":
            self.notifyToRemoteCaller(EVENT_NOTIFY_MSG,
                                      "    Loan eligibility criteria satisfied,"
                                      " please send another claim "
                                      "'Loan-Application-KYC'\n",
                                      self.wallet.defaultId, frm)


def create_thrift(name=None, wallet=None, base_dir_path=None, port=7777, client=None):

    endpoint_args = {'onlyListener': True}
    if wallet:
        endpoint_args['seed'] = wallet._signerById(wallet.defaultId).seed
    else:
        wallet = Wallet(name)
        wallet.addIdentifier(signer=SimpleSigner(seed=THRIFT_SEED))
        endpoint_args['seed'] = THRIFT_SEED

    if client is None:
        client = create_client(base_dir_path=None, client_class=TestClient)

    agent = ThriftAgent(name=name or 'Thrift Bank',
                        basedirpath=base_dir_path,
                        client=client,
                        wallet=wallet,
                        port=port,
                        endpointArgs=endpoint_args)

    agent._invites = {
        "77fbf9dc8c8e6acde33de98c6d747b28c": (1, "Alice"),
        "ousezru20ic4yz3j074trcgthwlsnfsef": (2, "Bob")
    }

    return agent

async def bootstrap_thrift(agent):
    pass

if __name__ == "__main__":
    args = RunnableAgent.parser_cmd_args()
    name = 'Thrift Bank'
    port = args.port
    if port is None:
        port = 7777
    with_cli = args.withcli
    agent = create_thrift(name=name, wallet=buildThriftWallet(),
                          base_dir_path=None, port=port)
    RunnableAgent.run_agent(agent, bootstrap=bootstrap_thrift(agent),
                            with_cli=with_cli)
