/* eslint-disable no-unused-vars */
import Service from '@/services/register_server_service';
const service = new Service();

export default {
    async initRegisterServer ({ commit }) {
        try {
            const { registered, registerServer, adminName, isAdmin } = await service.registerInfo();
            await commit('initRegisterServer', { registered, registerServer, adminName, isAdmin });
        } catch (error) {
            await commit('initRegisterServer', {});
        }
    },
    async createRegisterServer ({ commit }, data) {
        return await service.create(data);
    },
    async resendKeyRegisterServer ({ commit }) {
        return await service.resendKey();
    }
};
